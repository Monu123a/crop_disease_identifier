import React, { useRef, useState, useEffect } from 'react';
import './CameraUpload.css';

const CameraUpload = ({ onImageCapture, selectedImage, loading }) => {
    const [isCameraActive, setIsCameraActive] = useState(false);
    const [cameraError, setCameraError] = useState(null);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const galleryInputRef = useRef(null);
    const streamRef = useRef(null);

    const stopCamera = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
            streamRef.current = null;
        }
        setIsCameraActive(false);
    };

    const startCamera = async () => {
        setCameraError(null);
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' },
                audio: false
            });
            videoRef.current.srcObject = stream;
            streamRef.current = stream;
            setIsCameraActive(true);
        } catch (err) {
            console.error("Camera access error:", err);
            setCameraError("Could not access camera. Please check permissions.");
        }
    };

    const capturePhoto = () => {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        if (video && canvas) {
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            canvas.toBlob((blob) => {
                const file = new File([blob], "captured_leaf.jpg", { type: "image/jpeg" });
                const imageUrl = URL.createObjectURL(blob);
                onImageCapture(file, imageUrl);
                stopCamera();
            }, 'image/jpeg', 0.95);
        }
    };

    const handleGalleryUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            onImageCapture(file, imageUrl);
            stopCamera();
        }
    };

    const triggerGallery = () => galleryInputRef.current.click();

    useEffect(() => {
        return () => stopCamera();
    }, []);

    return (
        <div className="camera-upload-card glass-panel">
            <div className="preview-area">
                {isCameraActive ? (
                    <div className="camera-viewfinder">
                        <video
                            ref={videoRef}
                            autoPlay
                            playsInline
                            className="live-video"
                        />
                        <div className="camera-controls-overlay">
                            <button className="capture-trigger" onClick={capturePhoto}>
                                <div className="inner-circle"></div>
                            </button>
                            <button className="close-camera" onClick={stopCamera}>✕</button>
                        </div>
                    </div>
                ) : selectedImage ? (
                    <div className="image-wrapper">
                        <img src={selectedImage} alt="Crop preview" className="image-preview" />
                        <div className="preview-overlay">Preview</div>
                    </div>
                ) : (
                    <div className="placeholder-content">
                        <div className="icon-circle">
                            <span className="icon">🌿</span>
                        </div>
                        <h3>Scan your crop</h3>
                        <p>Use your camera to diagnose plant diseases instantly</p>
                        {cameraError && <p className="camera-error">{cameraError}</p>}
                    </div>
                )}
            </div>

            <canvas ref={canvasRef} style={{ display: 'none' }} />

            <div className="upload-controls">
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleGalleryUpload}
                    ref={galleryInputRef}
                    style={{ display: 'none' }}
                />

                {!selectedImage && !isCameraActive ? (
                    <div className="button-group">
                        <button className="primary-btn" onClick={startCamera} disabled={loading}>
                            <span className="btn-icon">📷</span> Open Camera
                        </button>
                        <button className="secondary-btn" onClick={triggerGallery} disabled={loading}>
                            <span className="btn-icon">📁</span> Upload from Files
                        </button>
                    </div>
                ) : (
                    <div className="button-group">
                        {!isCameraActive && (
                            <>
                                <button className="secondary-btn outline" onClick={startCamera} disabled={loading}>
                                    Take New Photo
                                </button>
                                <button className="secondary-btn outline" onClick={triggerGallery} disabled={loading}>
                                    Pick Different
                                </button>
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default CameraUpload;
