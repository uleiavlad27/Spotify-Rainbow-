import React, { useState, FormEvent } from "react";

interface ColorPickerProps {
  onSubmit: (data: { numSongs: number; targetColor: string }) => void;
}

const SpinnerIcon: React.FC = () => (
  <div className="spinner inline-block" />
);

const ColorPicker: React.FC<ColorPickerProps> = ({ onSubmit }) => {
  const [numSongs, setNumSongs] = useState<number>(20);
  const [targetColor, setTargetColor] = useState<string>("#ff0000");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await onSubmit({ numSongs, targetColor });
    } catch (error) {
      console.error("Error processing songs:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form 
      onSubmit={handleSubmit} 
      className="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto"
    >
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1">
          Number of Songs:
        </label>
        <input
          type="number"
          value={numSongs}
          onChange={(e) => setNumSongs(Number(e.target.value))}
          min="1"
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1">
          Choose a Target Color:
        </label>
        <input
          type="color"
          value={targetColor}
          onChange={(e) => setTargetColor(e.target.value)}
          className="border border-gray-300 rounded cursor-pointer"
        />
      </div>
      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-500 text-white font-semibold px-4 py-2 rounded hover:bg-blue-600 transition-colors"
      >
        {isLoading ? <SpinnerIcon /> : "Find Matching Songs"}
      </button>
    </form>
  );
};

export default ColorPicker;
