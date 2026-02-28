import React, { useRef } from 'react';
import './CameraUpload.css';

const CameraUpload = ({ onImageCapture, selectedImage, loading }) => {
    const cameraInputRef = useRef(null);
    const galleryInputRef = useRef(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            onImageCapture(file, imageUrl);
        }
    };

    const triggerCamera = () => cameraInputRef.current.click();
    const triggerGallery = () => galleryInputRef.current.click();

    return (
        <div className="camera-upload-card glass-panel">
            <div className="preview-area">
                {selectedImage ? (
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
                        <p>Take a clear photo of the affected leaf to get instance diagnosis</p>
                    </div>
                )}
            </div>

            <div className="upload-controls">
                {/* Hidden inputs */}
                <input
                    type="file"
                    accept="image/*"
                    capture="environment"
                    onChange={handleFileChange}
                    ref={cameraInputRef}
                    style={{ display: 'none' }}
                />
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    ref={galleryInputRef}
                    style={{ display: 'none' }}
                />

                {!selectedImage ? (
                    <div className="button-group">
                        <button className="primary-btn" onClick={triggerCamera} disabled={loading}>
                            <span className="btn-icon">📷</span> Take Photo
                        </button>
                        <button className="secondary-btn" onClick={triggerGallery} disabled={loading}>
                            <span className="btn-icon">📁</span> Upload Image
                        </button>
                    </div>
                ) : (
                    <div className="button-group">
                        <button className="secondary-btn outline" onClick={triggerCamera} disabled={loading}>
                            Retake
                        </button>
                        <button className="secondary-btn outline" onClick={triggerGallery} disabled={loading}>
                            Pick Different
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CameraUpload;
