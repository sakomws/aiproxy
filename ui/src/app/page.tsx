import React, { useState, FormEvent } from 'react';

// Define response interfaces
interface PredictResponse {
  chosen_model?: string;
  result?: string;
  current_usage_cost?: number;
}

interface UpdateWeightsResponse {
  message: string;
  new_weights: {
    alpha1: number;
    alpha2: number;
    alpha3: number;
    alpha4: number;
    alpha5: number;
    alpha6: number;
  };
}

const Home: React.FC = () => {
  // State for Predict
  const [predictText, setPredictText] = useState('');
  const [predictResult, setPredictResult] = useState('');
  const [chosenModel, setChosenModel] = useState('');
  const [currentUsageCost, setCurrentUsageCost] = useState<number | null>(null);
  const [loadingPredict, setLoadingPredict] = useState(false);
  const [predictError, setPredictError] = useState<string | null>(null);

  // State for Weights
  const [alpha1, setAlpha1] = useState<number>(2.0);
  const [alpha2, setAlpha2] = useState<number>(1.0);
  const [alpha3, setAlpha3] = useState<number>(1.5);
  const [alpha4, setAlpha4] = useState<number>(0.5);
  const [alpha5, setAlpha5] = useState<number>(1.0);
  const [alpha6, setAlpha6] = useState<number>(1.2);
  const [apiKey, setApiKey] = useState('secret-weight-key');
  const [updateMsg, setUpdateMsg] = useState('');
  const [loadingWeights, setLoadingWeights] = useState(false);
  const [weightsError, setWeightsError] = useState<string | null>(null);

  // ----------------------------------------------------------
  // Handler: Predict
  // ----------------------------------------------------------
  const handlePredict = async (e: FormEvent) => {
    e.preventDefault();
    setLoadingPredict(true);
    setPredictError(null);
    setPredictResult('');
    setChosenModel('');
    setCurrentUsageCost(null);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: predictText }),
      });
      if (!response.ok) {
        // Could parse error details from the response body if available
        throw new Error(`Server returned status ${response.status}`);
      }

      const data = (await response.json()) as PredictResponse;
      setChosenModel(data.chosen_model || '');
      setPredictResult(data.result || '');
      setCurrentUsageCost(data.current_usage_cost ?? 0);
    } catch (err: any) {
      console.error('Predict error:', err);
      setPredictError(err.message ?? 'Unknown error occurred');
    } finally {
      setLoadingPredict(false);
    }
  };

  // ----------------------------------------------------------
  // Handler: Update Weights
  // ----------------------------------------------------------
  const handleUpdateWeights = async (e: FormEvent) => {
    e.preventDefault();
    setLoadingWeights(true);
    setUpdateMsg('');
    setWeightsError(null);

    try {
      const payload = {
        alpha1,
        alpha2,
        alpha3,
        alpha4,
        alpha5,
        alpha6,
      };

      const url = `http://localhost:8000/update_weights?api_key=${encodeURIComponent(apiKey)}`;
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      const data = (await response.json()) as UpdateWeightsResponse;
      setUpdateMsg(`Weights updated: ${JSON.stringify(data.new_weights)}`);
    } catch (err: any) {
      console.error('Update weights error:', err);
      setWeightsError(err.message ?? 'Unknown error occurred');
    } finally {
      setLoadingWeights(false);
    }
  };

  // ----------------------------------------------------------
  // Render
  // ----------------------------------------------------------
  return (
    <div className="max-w-2xl mx-auto p-6 space-y-10">
      <h1 className="text-2xl font-bold text-center mb-4">
        AI Proxy UI (FastAPI + Next.js + Tailwind CSS)
      </h1>

      {/* Predict Section */}
      <section className="border border-gray-300 p-4 rounded-lg shadow-sm">
        <h2 className="text-xl font-semibold mb-2">Predict</h2>

        <form onSubmit={handlePredict} className="space-y-4">
          <div>
            <label htmlFor="predictText" className="block font-medium mb-1">
              Text to Predict:
            </label>
            <input
              id="predictText"
              type="text"
              value={predictText}
              onChange={(e) => setPredictText(e.target.value)}
              placeholder="Enter text..."
              className="border border-gray-400 rounded p-2 w-full"
            />
          </div>

          <button
            type="submit"
            disabled={loadingPredict}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loadingPredict ? 'Predicting...' : 'Predict'}
          </button>
        </form>

        {/* Display Prediction Result or Errors */}
        <div className="mt-4">
          {predictError && (
            <p className="text-red-600 font-semibold">
              Error: {predictError}
            </p>
          )}

          {predictResult && (
            <>
              <p className="mt-2">
                <strong>Chosen Model:</strong> {chosenModel}
              </p>
              <p>
                <strong>Result:</strong> {predictResult}
              </p>
              <p>
                <strong>Current Usage Cost:</strong> {currentUsageCost}
              </p>
            </>
          )}
        </div>
      </section>

      {/* Update Weights Section */}
      <section className="border border-gray-300 p-4 rounded-lg shadow-sm">
        <h2 className="text-xl font-semibold mb-2">Update Weights</h2>

        <form onSubmit={handleUpdateWeights} className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label htmlFor="alpha1" className="block font-medium mb-1">
                Alpha 1 (Acc):
              </label>
              <input
                id="alpha1"
                type="number"
                step="0.1"
                value={alpha1}
                onChange={(e) => setAlpha1(parseFloat(e.target.value))}
                className="border border-gray-400 rounded p-2 w-full"
              />
            </div>

            <div>
              <label htmlFor="alpha2" className="block font-medium mb-1">
                Alpha 2 (Lat):
              </label>
              <input
                id="alpha2"
                type="number"
                step="0.1"
                value={alpha2}
                onChange={(e) => setAlpha2(parseFloat(e.target.value))}
                className="border border-gray-400 rounded p-2 w-full"
              />
            </div>

            <div>
              <label htmlFor="alpha3" className="block font-medium mb-1">
                Alpha 3 (Cost):
              </label>
              <input
                id="alpha3"
                type="number"
                step="0.1"
                value={alpha3}
                onChange={(e) => setAlpha3(parseFloat(e.target.value))}
                className="border border-gray-400 rounded p-2 w-full"
              />
            </div>

            <div>
              <label htmlFor="alpha4" className="block font-medium mb-1">
                Alpha 4 (Load):
              </label>
              <input
                id="alpha4"
                type="number"
                step="0.1"
                value={alpha4}
                onChange={(e) => setAlpha4(parseFloat(e.target.value))}
                className="border border-gray-400 rounded p-2 w-full"
              />
            </div>

            <div>
              <label htmlFor="alpha5" className="block font-medium mb-1">
                Alpha 5 (Comp):
              </label>
              <input
                id="alpha5"
                type="number"
                step="0.1"
                value={alpha5}
                onChange={(e) => setAlpha5(parseFloat(e.target.value))}
                className="border border-gray-400 rounded p-2 w-full"
              />
            </div>

            <div>
              <label htmlFor="alpha6" className="block font-medium mb-1">
                Alpha 6 (Conf):
              </label>
              <input
                id="alpha6"
                type="number"
                step="0.1"
                value={alpha6}
                onChange={(e) => setAlpha6(parseFloat(e.target.value))}
                className="border border-gray-400 rounded p-2 w-full"
              />
            </div>
          </div>

          <div>
            <label htmlFor="apiKey" className="block font-medium mb-1">
              API Key:
            </label>
            <input
              id="apiKey"
              type="text"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="border border-gray-400 rounded p-2 w-full"
              placeholder="secret-weight-key"
            />
          </div>

          <button
            type="submit"
            disabled={loadingWeights}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
          >
            {loadingWeights ? 'Updating...' : 'Update Weights'}
          </button>
        </form>

        {/* Display Update Result or Errors */}
        <div className="mt-4">
          {weightsError && (
            <p className="text-red-600 font-semibold">Error: {weightsError}</p>
          )}
          {updateMsg && (
            <p className="text-green-700 font-semibold">{updateMsg}</p>
          )}
        </div>
      </section>
    </div>
  );
};

export default Home;
