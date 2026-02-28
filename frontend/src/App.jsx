import React, { useState } from 'react';
import axios from 'axios';
import './styles/theme.css';
import './App.css';
import CameraUpload from './components/CameraUpload';
import ResultCard from './components/ResultCard';
import Loader from './components/Loader';

const API_ENDPOINT = 'http://localhost:5000/analyze';

function App() {
  const [imageFile, setImageFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageCapture = (file, url) => {
    setImageFile(file);
    setPreviewUrl(url);
    setResult(null);
    setError(null);
  };

  const analyzeDisease = async () => {
    if (!imageFile) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', imageFile);

    try {
      const response = await axios.post(API_ENDPOINT, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      // Handle the potentially more complex response
      setResult(response.data);
    } catch (err) {
      console.error('Analysis failed:', err);
      // For demonstration let's mock a result if the API is not running
      // Remove this mock in production
      /*
      setResult({
        disease: "Tomato Late Blight",
        severity: "High",
        confidence: 94,
        treatment: "Apply fungicide containing chlorothalonil or copper. Remove and destroy infected plants to prevent spread.",
        affectedCrops: "Tomatoes, Potatoes, Peppers",
        prevention: "Use resistant varieties, improve air circulation, and avoid overhead watering.",
        nextSteps: ["Isolate the crop area", "Clean all farming tools", "Apply preventative spray to nearby healthy plants"]
      });
      */
      setError('Could not connect to the analysis server. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const resetAll = () => {
    setImageFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="container">
      <header>
        <h1>CropScope</h1>
        <p className="subtitle">AI Crop Disease Identifier</p>
      </header>

      <div className={`app-content ${result ? 'has-result' : ''}`}>
        <section className="interaction-section">
          <CameraUpload
            onImageCapture={handleImageCapture}
            selectedImage={previewUrl}
            loading={loading}
          />

          {previewUrl && !loading && !result && (
            <button className="analyze-btn" onClick={analyzeDisease}>
              <span className="btn-icon">⚡</span> Analyze Leaf
            </button>
          )}

          {error && <div className="error-message glass-panel">{error}</div>}
        </section>

        {result && (
          <section className="result-section">
            <ResultCard result={result} onReset={resetAll} />
          </section>
        )}
      </div>

      {loading && <Loader />}

      <footer>
        <p>© 2026 CropScope • Powered by AI for Sustainable Farming</p>
      </footer>
    </div>
  );
}

export default App;
