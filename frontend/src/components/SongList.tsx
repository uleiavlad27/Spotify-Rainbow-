import React from "react";

interface Song {
  name: string;
  image_url: string | null;
}

interface SongListProps {
  songs: {
    [color: string]: Song;
  };
}

const SongList: React.FC<SongListProps> = ({ songs }) => {
  return (
    <div className="p-6 bg-gray-600 rounded-xl">
      <h2 className="text-2xl font-bold mb-4 text-gray-300">Matched Songs</h2>
      <ul className="space-y-4">
        {Object.entries(songs).map(([color, song], index) => (
          <li
            key={color}
            className="p-4 rounded-md  bg-gray-700/50"
          >
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gray-200 flex items-center justify-center rounded-full">
                <span className="text-xs font-semibold text-gray-700">
                  {index + 1}
                </span>
              </div>
              <div>
                <p className="font-medium text-lg text-gray-300">{song.name}</p>
                {song.image_url && (
                  <div className="mt-2">
                    <img
                      src={song.image_url}
                      alt={song.name}
                      className="w-36 rounded"
                    />
                  </div>
                )}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SongList;
