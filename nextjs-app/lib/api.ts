import { SignupResponse, SigninResponse } from '../types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export const api = {
  async signup(email: string, image: File): Promise<SignupResponse> {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('image', image);

    const response = await fetch(`${API_URL}/api/auth/signup`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new ApiError(response.status, error.detail);
    }

    return response.json();
  },

  async signin(email: string, image: File): Promise<SigninResponse> {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('image', image);

    const response = await fetch(`${API_URL}/api/auth/signin`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new ApiError(response.status, error.detail);
    }

    return response.json();
  },

  async checkEmail(email: string): Promise<{ exists: boolean }> {
    const response = await fetch(
      `${API_URL}/api/auth/check-email?email=${encodeURIComponent(email)}`
    );

    if (!response.ok) {
      throw new Error('Failed to check email');
    }

    return response.json();
  }
};

export { ApiError };
