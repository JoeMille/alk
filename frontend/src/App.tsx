import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/Auth/Login'
import Register from './components/Auth/Register'
import GroupsList from './components/Groups/GroupsList'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/groups" element={<GroupsList />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App