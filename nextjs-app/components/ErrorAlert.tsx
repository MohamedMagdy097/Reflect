import React from 'react';

interface ErrorAlertProps {
  message: string;
}

export const ErrorAlert: React.FC<ErrorAlertProps> = ({ message }) => {
  return (
    <div className="error-alert">
      <span className="error-icon">!</span>
      <p>{message}</p>
    </div>
  );
};
