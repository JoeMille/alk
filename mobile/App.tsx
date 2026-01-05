import React from 'react';
import LoginScreen from './src/screens/Auth/LoginScreen';

function App(): React.JSX.Element {
  const mockNavigation = {
    navigate: (screen: string) => console.log('Navigate to:', screen),
    replace: (screen: string) => console.log('Replace with:', screen),
  };

  return <LoginScreen navigation={mockNavigation} />;
}

export default App;