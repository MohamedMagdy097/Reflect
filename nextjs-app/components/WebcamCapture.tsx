import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

interface WebcamCaptureProps {
  onCapture: (file: File) => void;
  disabled?: boolean;
}

export const WebcamCapture: React.FC<WebcamCaptureProps> = ({
  onCapture,
  disabled = false
}) => {
  const webcamRef = useRef<Webcam>(null);
  const [imgSrc, setImgSrc] = useState<string | null>(null);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);

  const videoConstraints = {
    width: 640,
    height: 480,
    facingMode: "user"
  };

  const handleUserMedia = () => {
    setHasPermission(true);
  };

  const handleUserMediaError = () => {
    setHasPermission(false);
  };

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setImgSrc(imageSrc);

        // Convert base64 to File object
        fetch(imageSrc)
          .then(res => res.blob())
          .then(blob => {
            const file = new File([blob], "face-capture.jpg", {
              type: "image/jpeg"
            });
            onCapture(file);
          });
      }
    }
  }, [webcamRef, onCapture]);

  const retake = () => {
    setImgSrc(null);
  };

  if (hasPermission === false) {
    return (
      <div className="webcam-error">
        <p>Camera access denied. Please enable camera permissions to continue.</p>
      </div>
    );
  }

  return (
    <div className="webcam-container">
      {!imgSrc ? (
        <>
          <Webcam
            ref={webcamRef}
            audio={false}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
            className="webcam-video"
            onUserMedia={handleUserMedia}
            onUserMediaError={handleUserMediaError}
          />
          <button
            type="button"
            onClick={capture}
            disabled={disabled || !hasPermission}
            className="btn-capture"
          >
            Capture Photo
          </button>
        </>
      ) : (
        <>
          <img src={imgSrc} alt="Captured face" className="captured-image" />
          <button
            type="button"
            onClick={retake}
            disabled={disabled}
            className="btn-retake"
          >
            Retake Photo
          </button>
        </>
      )}
    </div>
  );
};
