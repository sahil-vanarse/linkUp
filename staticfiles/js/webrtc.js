class WebRTCHandler {
    constructor(roomId, userId) {
        this.roomId = roomId;
        this.userId = userId;
        this.peers = {};
        this.localStream = null;
        this.configuration = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' }
            ]
        };

        this.audioEnabled = true;
        this.videoEnabled = true;

        this.initSignaling();
        this.setupUIHandlers();
    }

    async requestMediaPermissions() {
        try {
            await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            return true;
        } catch (error) {
            console.error('Permission denied:', error);
            return false;
        }
    }

    initSignaling() {
        this.signalingSocket = new WebSocket(
            `wss://${window.location.host}/ws/base/room/${this.roomId}/webrtc/`
        );

        this.signalingSocket.onmessage = async (event) => {
            const data = JSON.parse(event.data);
            
            switch (data.type) {
                case 'offer':
                    await this.handleOffer(data);
                    break;
                case 'answer':
                    await this.handleAnswer(data);
                    break;
                case 'ice-candidate':
                    await this.handleIceCandidate(data);
                    break;
                case 'user-joined':
                    await this.handleNewUser(data.userId);
                    break;
                case 'user-left':
                    this.handleUserLeft(data.userId);
                    break;
                case 'call-request':
                    this.showCallNotification(data.userId);
                    break;
            }
        };
    }

    async handleNewUser(userId) {
        if (userId === this.userId) return;

        const peer = await this.createPeerConnection(userId);
        const offer = await peer.createOffer();
        await peer.setLocalDescription(offer);

        this.signalingSocket.send(JSON.stringify({
            message: {
                type: 'offer',
                offer: peer.localDescription,
                target: userId
            }
        }));
    }

    setupUIHandlers() {
        const videoCallBtn = document.getElementById('videoCallBtn');
        const joinCallBtn = document.getElementById('joinVideoCallBtn');
        const declineCallBtn = document.getElementById('declineVideoCallBtn');
        const endCallBtn = document.getElementById('endCall');
        const toggleAudioBtn = document.getElementById('toggleAudio');
        const toggleVideoBtn = document.getElementById('toggleVideo');

        videoCallBtn?.addEventListener('click', async () => {
            const hasPermissions = await this.requestMediaPermissions();
            if (hasPermissions) {
                await this.startCall();
                this.broadcastCallRequest();
            } else {
                alert('Camera and microphone permissions are required for video calls.');
            }
        });

        joinCallBtn?.addEventListener('click', async () => {
            const hasPermissions = await this.requestMediaPermissions();
            if (hasPermissions) {
                await this.joinCall();
                document.getElementById('videoCallNotification').style.display = 'none';
            } else {
                alert('Camera and microphone permissions are required for video calls.');
            }
        });

        declineCallBtn?.addEventListener('click', () => {
            document.getElementById('videoCallNotification').style.display = 'none';
        });

        endCallBtn?.addEventListener('click', () => this.endCall());

        toggleAudioBtn?.addEventListener('click', () => this.toggleAudio());
        toggleVideoBtn?.addEventListener('click', () => this.toggleVideo());
    }

    async startCall() {
        try {
            this.localStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            
            document.getElementById('callContainer').style.display = 'block';
            this.showLocalVideo();
            this.setupPeerConnections();
            
            const toggleAudioBtn = document.getElementById('toggleAudio');
            const toggleVideoBtn = document.getElementById('toggleVideo');
            
            toggleAudioBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            toggleVideoBtn.innerHTML = '<i class="fas fa-video"></i>';
        } catch (error) {
            console.error('Error starting call:', error);
            alert('Failed to access camera or microphone. Please check permissions.');
        }
    }

    broadcastCallRequest() {
        this.signalingSocket.send(JSON.stringify({
            message: {
                type: 'call-request',
                sender: this.userId
            }
        }));
    }

    showCallNotification(callerId) {
        const notification = document.getElementById('videoCallNotification');
        notification.style.display = 'block';
    }

    async createPeerConnection(userId) {
        const peer = new RTCPeerConnection(this.configuration);
        this.peers[userId] = peer;

        this.localStream.getTracks().forEach(track => {
            peer.addTrack(track, this.localStream);
        });

        peer.onicecandidate = (event) => {
            if (event.candidate) {
                this.signalingSocket.send(JSON.stringify({
                    message: {
                        type: 'ice-candidate',
                        candidate: event.candidate,
                        target: userId
                    }
                }));
            }
        };

        peer.ontrack = (event) => {
            const remoteStream = event.streams[0];
            this.showRemoteVideo(userId, remoteStream);
        };

        return peer;
    }

    async handleOffer(data) {
        const peer = await this.createPeerConnection(data.sender);
        await peer.setRemoteDescription(new RTCSessionDescription(data.offer));
        const answer = await peer.createAnswer();
        await peer.setLocalDescription(answer);

        this.signalingSocket.send(JSON.stringify({
            message: {
                type: 'answer',
                answer: answer,
                target: data.sender
            }
        }));
    }

    showLocalVideo() {
        const videoGrid = document.querySelector('.video-grid');
        const videoContainer = document.createElement('div');
        videoContainer.className = 'video-container';
        videoContainer.id = `local-${this.userId}`;
        
        const video = document.createElement('video');
        video.autoplay = true;
        video.playsInline = true;
        video.muted = true;
        video.srcObject = this.localStream;
        
        const label = document.createElement('div');
        label.className = 'video-label';
        label.textContent = 'You';
        
        videoContainer.appendChild(video);
        videoContainer.appendChild(label);
        videoGrid.appendChild(videoContainer);
        
        video.play().catch(e => console.error('Error playing local video:', e));
    }

    showRemoteVideo(userId, stream) {
        const videoGrid = document.querySelector('.video-grid');
        const existingContainer = document.getElementById(`remote-${userId}`);
        
        if (!existingContainer) {
            const videoContainer = document.createElement('div');
            videoContainer.className = 'video-container';
            videoContainer.id = `remote-${userId}`;
            
            const video = document.createElement('video');
            video.autoplay = true;
            video.playsInline = true;
            video.srcObject = stream;
            
            const label = document.createElement('div');
            label.className = 'video-label';
            label.textContent = `User ${userId}`;
            
            videoContainer.appendChild(video);
            videoContainer.appendChild(label);
            videoGrid.appendChild(videoContainer);
            
            video.play().catch(e => console.error('Error playing remote video:', e));
        }
    }

    toggleAudio() {
        if (this.localStream) {
            const audioTrack = this.localStream.getAudioTracks()[0];
            if (audioTrack) {
                audioTrack.enabled = !audioTrack.enabled;
                this.audioEnabled = audioTrack.enabled;
                
                const toggleAudioBtn = document.getElementById('toggleAudio');
                toggleAudioBtn.innerHTML = this.audioEnabled ? 
                    '<i class="fas fa-microphone"></i>' : 
                    '<i class="fas fa-microphone-slash"></i>';
            }
        }
    }

    toggleVideo() {
        if (this.localStream) {
            const videoTrack = this.localStream.getVideoTracks()[0];
            if (videoTrack) {
                videoTrack.enabled = !videoTrack.enabled;
                this.videoEnabled = videoTrack.enabled;
                
                const toggleVideoBtn = document.getElementById('toggleVideo');
                toggleVideoBtn.innerHTML = this.videoEnabled ? 
                    '<i class="fas fa-video"></i>' : 
                    '<i class="fas fa-video-slash"></i>';
            }
        }
    }

    handleUserLeft(userId) {
        const videoElement = document.getElementById(`remote-${userId}`);
        if (videoElement) {
            videoElement.remove();
        }
        
        if (this.peers[userId]) {
            this.peers[userId].close();
            delete this.peers[userId];
        }
    }

    endCall() {
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
        }

        Object.values(this.peers).forEach(peer => {
            if (peer) {
                peer.close();
            }
        });
        this.peers = {};

        const videoGrid = document.querySelector('.video-grid');
        while (videoGrid.firstChild) {
            videoGrid.removeChild(videoGrid.firstChild);
        }

        document.getElementById('callContainer').style.display = 'none';

        this.audioEnabled = true;
        this.videoEnabled = true;
    }
}

export default WebRTCHandler;