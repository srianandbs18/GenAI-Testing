/**
 * AudioRecorder
 * Captures microphone input and converts it to 16-bit PCM (Linear PCM).
 * Uses AudioWorklet or ScriptProcessor (fallback) for raw data access.
 */
export class AudioRecorder {
    constructor() {
        this.mediaStream = null;
        this.audioContext = null;
        this.processor = null;
        this.input = null;
        this.audioData = []; // Stores Int16 chunks
        this.recording = false;
        this.sampleRate = 24000; // Target sample rate
    }

    async start() {
        try {
            this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
                sampleRate: this.sampleRate,
            });

            this.input = this.audioContext.createMediaStreamSource(this.mediaStream);

            // Use ScriptProcessor for simplicity (deprecated but widely supported for this demo)
            // Buffer size 4096
            this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);

            this.audioData = [];
            this.recording = true;

            this.processor.onaudioprocess = (e) => {
                if (!this.recording) return;
                const inputData = e.inputBuffer.getChannelData(0);
                this.audioData.push(this._floatTo16BitPCM(inputData));
            };

            this.input.connect(this.processor);
            this.processor.connect(this.audioContext.destination);

            console.log("Recording started at", this.audioContext.sampleRate, "Hz");
            return true;
        } catch (error) {
            console.error("Error starting recording:", error);
            return false;
        }
    }

    stop() {
        this.recording = false;
        if (this.mediaStream) {
            this.mediaStream.getTracks().forEach(track => track.stop());
        }
        if (this.processor && this.input) {
            this.input.disconnect();
            this.processor.disconnect();
        }
        if (this.audioContext) {
            this.audioContext.close();
        }
        console.log("Recording stopped");
        return this._mergeAudioData();
    }

    _floatTo16BitPCM(input) {
        const output = new Int16Array(input.length);
        for (let i = 0; i < input.length; i++) {
            const s = Math.max(-1, Math.min(1, input[i]));
            output[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
        }
        return output;
    }

    _mergeAudioData() {
        const totalLength = this.audioData.reduce((acc, chunk) => acc + chunk.length, 0);
        const result = new Int16Array(totalLength);
        let offset = 0;
        for (const chunk of this.audioData) {
            result.set(chunk, offset);
            offset += chunk.length;
        }
        return result;
    }

    // Helper to convert Int16Array to Base64 string
    static toBase64(int16Array) {
        const buffer = int16Array.buffer;
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }
}
