import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, File, X } from 'lucide-react';

const FileUpload = ({ onFileSelect, acceptedTypes = '.pdf,.doc,.docx' }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    setSelectedFile(file);
    onFileSelect(file);
  };

  const removeFile = () => {
    setSelectedFile(null);
    onFileSelect(null);
  };

  return (
    <div className="w-full">
      <div
        className={`relative border-2 border-dashed rounded-xl p-8 transition-all duration-300 ${
          dragActive
            ? 'border-purple-500 bg-purple-500/10'
            : 'border-white/20 hover:border-purple-500/50'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          accept={acceptedTypes}
          onChange={handleChange}
        />

        {!selectedFile ? (
          <label
            htmlFor="file-upload"
            className="flex flex-col items-center cursor-pointer"
          >
            <motion.div
              whileHover={{ scale: 1.1 }}
              className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-500/20 to-blue-500/20 flex items-center justify-center mb-4"
            >
              <Upload className="w-8 h-8 text-purple-400" />
            </motion.div>
            <p className="text-white font-medium mb-2">
              Drop your resume here or click to browse
            </p>
            <p className="text-gray-400 text-sm">
              Supports PDF, DOC, DOCX (Max 10MB)
            </p>
          </label>
        ) : (
          <div className="flex items-center justify-between glass rounded-lg p-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500/20 to-blue-500/20 flex items-center justify-center">
                <File className="w-5 h-5 text-purple-400" />
              </div>
              <div>
                <p className="text-white font-medium text-sm">
                  {selectedFile.name}
                </p>
                <p className="text-gray-400 text-xs">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="text-gray-400 hover:text-red-400 transition-colors"
            >
              <X size={20} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
