class WebRTCHandler {
    constructor(roomId) {
        this.roomId = roomId;
        this.localStream = null;
        this.remoteStream = null;
        this.peerConnection = null;
        this.signalingSocket = null;

        this.configuration = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' }
            ]
        };

        this.init();
    }

    async init() {
        this.connectSignaling();
        this.setupPeerConnection();
    }

    connectSignaling() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.signalingSocket = new WebSocket(
            `${wsProtocol}//${window.location.host}/ws/base/room/${this.roomId}/webrtc/`
        );

        this.signalingSocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            switch (data.type) {
                case 'offer':
                    this.handleOffer(data);
                    break;
                case 'answer':
                    this.handleAnswer(data);
                    break;
                case 'ice-candidate':
                    this.handleIceCandidate(data);
                    break;
                case 'call-notification':
                    document.getElementById('callStarter').textContent = data.username;
                    document.getElementById('videoCallNotification').style.display = 'block';
                    break;
            }
        };
    }

    setupPeerConnection() {
        this.peerConnection = new RTCPeerConnection(this.configuration);

        this.peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                this.signalingSocket.send(JSON.stringify({
                    type: 'ice-candidate',
                    candidate: event.candidate
                }));
            }
        };

        this.peerConnection.ontrack = (event) => {
            const remoteVideo = document.getElementById('remoteVideo');
            if (remoteVideo.srcObject !== event.streams[0]) {
                remoteVideo.srcObject = event.streams[0];
                this.remoteStream = event.streams[0];
            }
        };
    }

    async startCall(isVideo = true) {
        try {
            const constraints = { audio: true, video: isVideo };

            this.localStream = await navigator.mediaDevices.getUserMedia(constraints);
            document.getElementById('localVideo').srcObject = this.localStream;

            this.localStream.getTracks().forEach(track => {
                this.peerConnection.addTrack(track, this.localStream);
            });

            const offer = await this.peerConnection.createOffer();
            await this.peerConnection.setLocalDescription(offer);

            this.signalingSocket.send(JSON.stringify({
                type: 'offer',
                offer: offer
            }));

            this.signalingSocket.send(JSON.stringify({
                type: 'start-call',
                username: roomId // Replace with the username of the call starter
            }));

            document.getElementById('callContainer').style.display = 'block';
        } catch (error) {
            console.error('Error starting call:', error);
            alert('Could not start call. Please check your camera/microphone permissions.');
        }
    }

    async handleOffer(data) {
        try {
            document.getElementById('callContainer').style.display = 'block';

            const constraints = { audio: true, video: true };

            this.localStream = await navigator.mediaDevices.getUserMedia(constraints);
            document.getElementById('localVideo').srcObject = this.localStream;

            this.localStream.getTracks().forEach(track => {
                this.peerConnection.addTrack(track, this.localStream);
            });

            await this.peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
            const answer = await this.peerConnection.createAnswer();
            await this.peerConnection.setLocalDescription(answer);

            this.signalingSocket.send(JSON.stringify({
                type: 'answer',
                answer: answer
            }));
        } catch (error) {
            console.error('Error handling offer:', error);
        }
    }

    async handleAnswer(data) {
        try {
            await this.peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
        } catch (error) {
            console.error('Error handling answer:', error);
        }
    }

    async handleIceCandidate(data) {
        try {
            await this.peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate));
        } catch (error) {
            console.error('Error handling ICE candidate:', error);
        }
    }

    endCall() {
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
        }
        if (this.peerConnection) {
            this.peerConnection.close();
        }
        document.getElementById('callContainer').style.display = 'none';

        this.signalingSocket.send(JSON.stringify({ type: 'end-call' }));
    }
}

// Initialize WebRTC
document.addEventListener('DOMContentLoaded', () => {
    const webrtc = new WebRTCHandler(roomId);

    document.getElementById('audioCallBtn').addEventListener('click', () => {
        webrtc.startCall(false);
    });

    document.getElementById('videoCallBtn').addEventListener('click', () => {
        webrtc.startCall(true);
    });

    document.getElementById('endCall').addEventListener('click', () => {
        webrtc.endCall();
    });

    document.getElementById('toggleAudio').addEventListener('click', (e) => {
        const audioTrack = webrtc.localStream.getAudioTracks()[0];
        audioTrack.enabled = !audioTrack.enabled;
        e.target.textContent = audioTrack.enabled ? 'Mute' : 'Unmute';
    });

    document.getElementById('toggleVideo').addEventListener('click', (e) => {
        const videoTrack = webrtc.localStream.getVideoTracks()[0];
        videoTrack.enabled = !videoTrack.enabled;
        e.target.textContent = videoTrack.enabled ? 'Stop Video' : 'Start Video';
    });

    document.getElementById('joinVideoCallBtn').addEventListener('click', () => {
        document.getElementById('callContainer').style.display = 'block';
    });
});
