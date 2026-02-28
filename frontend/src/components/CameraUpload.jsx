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
            streamRef.current = stream;
            setIsCameraActive(true); // triggers re-render → <video> mounts → useEffect attaches srcObject
        } catch (err) {
            console.error("Camera access error:", err);
            setCameraError("Could not access camera. Please check permissions.");
        }
    };

    // Attach the stream after the <video> element is rendered in the DOM
    useEffect(() => {
        if (isCameraActive && videoRef.current && streamRef.current) {
            videoRef.current.srcObject = streamRef.current;
            videoRef.current.play().catch((err) => {
                console.error("Video play error:", err);
                setCameraError("Could not start video stream. Please try again.");
            });
        }
    }, [isCameraActive]);

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


    /**
     * Convert any browser-displayable image to a JPEG File via Canvas.
     * This handles HEIC (macOS/Safari), WebP, AVIF, PNG, etc. so the
     * backend always receives a format that PIL can read.
     */
    const normaliseToJpeg = (rawFile) =>
        new Promise((resolve, reject) => {
            const url = URL.createObjectURL(rawFile);
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                canvas.getContext('2d').drawImage(img, 0, 0);
                URL.revokeObjectURL(url);
                canvas.toBlob((blob) => {
                    if (!blob) { reject(new Error('Canvas conversion failed')); return; }
                    const name = rawFile.name.replace(/\.[^.]+$/, '') + '.jpg';
                    resolve({ file: new File([blob], name, { type: 'image/jpeg' }), url: URL.createObjectURL(blob) });
                }, 'image/jpeg', 0.92);
            };
            img.onerror = () => { URL.revokeObjectURL(url); reject(new Error('Could not load image')); };
            img.src = url;
        });

    const handleGalleryUpload = async (event) => {
        const rawFile = event.target.files[0];
        if (!rawFile) return;
        // Reset input so the same file can be re-selected if needed
        event.target.value = '';
        try {
            const { file, url } = await normaliseToJpeg(rawFile);
            onImageCapture(file, url);
            stopCamera();
        } catch (err) {
            console.error('Image conversion error:', err);
            setCameraError('Could not read this image format. Please try a JPEG or PNG file.');
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
                            muted
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
