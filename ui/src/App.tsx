import { Route, Routes } from 'react-router-dom'
import './App.css'
import Chat from './pages/Chat'
import Login from './pages/Login'
import UploadDocument from './pages/UploadDocument'

function App() {

  return (
    <>
    <div>
      {/* <Navbar /> */}
      <Routes>
        {/* <Route path="/home" element={<Home />} /> */}
        <Route path="/" element={<Login />} />
        {/* <Route path="/logout" element={<Logout />} /> */}
        <Route path="/upload_document" element={<UploadDocument />} />
        <Route path="/chat" element={<Chat/>} />
        {/* <Route path="/signup" element={<SignUp />} /> */}
      </Routes>
    </div>
    </>
  )
}

export default App