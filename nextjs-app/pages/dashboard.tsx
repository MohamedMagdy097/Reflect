import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

interface UserData {
  email: string;
  userId: string;
  isNewUser: boolean;
}

export default function DashboardPage() {
  const router = useRouter();
  const [userData, setUserData] = useState<UserData | null>(null);

  useEffect(() => {
    const { email, userId, newUser } = router.query;

    if (!email || !userId) {
      // Redirect to signin if no user data
      router.push('/signin');
      return;
    }

    setUserData({
      email: email as string,
      userId: userId as string,
      isNewUser: newUser === 'true'
    });
  }, [router, router.query]);

  const handleSignOut = () => {
    router.push('/signin');
  };

  if (!userData) {
    return (
      <div className="container">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Welcome to Reflect!</h1>

      {userData.isNewUser && (
        <div className="success-message">
          Account created successfully!
        </div>
      )}

      <div className="user-info">
        <p><strong>Email:</strong> {userData.email}</p>
        <p><strong>User ID:</strong> {userData.userId}</p>
      </div>

      <p className="welcome-text">
        You&apos;ve successfully authenticated with face recognition.
      </p>

      <button
        onClick={handleSignOut}
        className="btn-secondary"
      >
        Sign Out
      </button>
    </div>
  );
}
