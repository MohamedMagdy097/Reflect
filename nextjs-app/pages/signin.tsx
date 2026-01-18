import { useState } from 'react';
import { useRouter } from 'next/router';
import { WebcamCapture } from '../components/WebcamCapture';
import { ErrorAlert } from '../components/ErrorAlert';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { api } from '../lib/api';

export default function SigninPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [capturedImage, setCapturedImage] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleCapture = (imageFile: File) => {
    setCapturedImage(imageFile);
    setError(null);
  };

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }

    if (!capturedImage) {
      setError('Please capture your face photo');
      return;
    }

    setIsLoading(true);

    try {
      const response = await api.signin(email, capturedImage);

      // Success - redirect to dashboard
      router.push({
        pathname: '/dashboard',
        query: {
          email: response.email,
          userId: response.user_id
        }
      });
    } catch (err: any) {
      // Handle specific error cases
      if (err.message.includes('different email')) {
        setError(err.message);
      } else if (err.message.includes('not registered')) {
        setError('Email not registered. Please sign up first.');
      } else if (err.message.includes('not recognized')) {
        setError('Face not recognized. Please try again.');
      } else if (err.message.includes('No face detected') || err.message.includes('no face')) {
        setError('No face detected. Please ensure your face is clearly visible and try again.');
      } else if (err.message.includes('Multiple faces')) {
        setError('Multiple faces detected. Please ensure only one face is visible.');
      } else {
        setError(err.message || 'Sign in failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Sign In</h1>

      {error && <ErrorAlert message={error} />}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="your.email@example.com"
            disabled={isLoading}
            required
          />
        </div>

        <div className="form-group">
          <label>Face Photo</label>
          <WebcamCapture
            onCapture={handleCapture}
            disabled={isLoading}
          />
        </div>

        <button
          type="submit"
          disabled={isLoading || !capturedImage}
          className="btn-primary"
        >
          {isLoading ? (
            <>
              <LoadingSpinner />
              Signing In...
            </>
          ) : (
            'Sign In'
          )}
        </button>
      </form>

      <p className="text-center">
        Don&apos;t have an account?{' '}
        <a href="/signup">Sign Up</a>
      </p>
    </div>
  );
}
