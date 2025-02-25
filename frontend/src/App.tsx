import React, { useState, useEffect } from "react";
import ColorPicker from "./components/ColorPicker.tsx";
import SongList from "./components/SongList.tsx";

interface MatchedSongs {
  [color: string]: {
    name: string;
    image_url: string | null;
  };
}

const App: React.FC = () => {
  const [token, setToken] = useState<string | null>(null);
  const [matchedSongs, setMatchedSongs] = useState<MatchedSongs | null>(null);

  // On mount, try to get the token from the URL (after Spotify callback).
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const tokenFromUrl = params.get("token");
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    }
  }, []);

  // Fetch the Spotify auth URL from your backend (via the proxy)
  const fetchAuthUrl = async () => {
    try {
      const response = await fetch("/api/auth-url");
      const data = await response.json();
      // Redirect to the Spotify authentication page.
      window.location.href = data.auth_url;
    } catch (error) {
      console.error("Error fetching auth URL:", error);
    }
  };

  // Handle form submission from ColorPicker and call your backend's process-songs endpoint.
  const handleColorSubmit = async ({ numSongs, targetColor }) => {
    if (!token) {
      alert("Please authenticate with Spotify first.");
      return;
    }
    try {
      const response = await fetch("/api/process-songs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Change "num_songs" to "total_tracks" and add "top_n" if needed.
        body: JSON.stringify({ token, total_tracks: numSongs, target_color: targetColor, top_n: 10 })
      });
      
      // Check if the response has content
      const text = await response.text();
      if (!text) {
        throw new Error("Empty response from the server");
      }
      const data = JSON.parse(text);
      setMatchedSongs(data);
    } catch (error) {
      console.error("Error processing songs:", error);
    }
  };
  

  return (
    <div className="bg-gradient-to-r from-slate-800 to-blue-950 min-h-screen p-6 flex flex-col items-center justify-center gap-6">
      <div className="text-6xl border border-gray-900/35 rounded-4xl bg-gray-900/35 p-4 text-center max-w-max">
        <div className="text-white pb-2">
          Spotify Rainbow Songs
        </div>
      </div>
  
      <div className="flex flex-col items-center gap-4">
        {!token && (
          <button 
            onClick={fetchAuthUrl} 
            className="text-2xl px-4 py-2 bg-emerald-800 text-white rounded-xl hover:bg-emerald-900"
          >
            Authenticate with Spotify
          </button>
        )}
        {token && (
          <>
            <ColorPicker onSubmit={handleColorSubmit} />
            {matchedSongs && <SongList songs={matchedSongs} />}
          </>
        )}
      </div>
    </div>
  );
  
  
};

export default App;
