import React from 'react';
import './Loader.css';

const Loader = () => {
    return (
        <div className="loader-overlay">
            <div className="loader-container">
                <div className="spinner"></div>
                <p>Analyzing leaf...</p>
            </div>
        </div>
    );
};

export default Loader;
