import React, { useState } from 'react';
import { analyzeVideo } from '../services/api';
import { AnalysisResult } from '../types';

const VideoUploader: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Por favor selecciona un video');
      return;
    }

    setLoading(true);
    try {
      const response = await analyzeVideo(file);
      setResult(response);
      setFile(null);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">Cargar Video para Análisis</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500">
          <input
            type="file"
            accept="video/*"
            onChange={handleFileChange}
            className="hidden"
            id="video-input"
          />
          <label htmlFor="video-input" className="cursor-pointer">
            <p className="text-gray-600">Arrastra tu video aquí o haz click</p>
            {file && <p className="text-green-600 mt-2">✓ {file.name}</p>}
          </label>
        </div>

        <button
          type="submit"
          disabled={loading || !file}
          className="w-full mt-4 bg-blue-500 text-white py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Analizando...' : 'Analizar Video'}
        </button>
      </form>

      {error && <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">{error}</div>}
      
      {result && (
        <div className="mt-4 p-4 bg-green-100 text-green-700 rounded">
          <h3 className="font-bold">Análisis Completado</h3>
          <p>Actividad: {result.activity.activity_type}</p>
          <p>Confianza: {(result.activity.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
};

export default VideoUploader;
