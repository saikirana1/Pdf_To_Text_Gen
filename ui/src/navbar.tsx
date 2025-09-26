import { Link, useNavigate } from "react-router-dom";

function Navbar() {

 return (
    
    <nav className="bg-pink-300 p-4 text-center">
      <div className="flex justify-between">
          <Link
            to="/"
            className="text-blue-800 hover:text-pink-700 font-medium"
          >
            Login
          </Link>
      
            {/* <Link
              to="/home"
              className="text-blue-800 hover:text-pink-700 font-medium"
            >
              Home
            </Link> */}

            <Link
              to="/chat"
              className="text-blue-800 hover:text-pink-700 font-medium"
            >
              Chat
            </Link>
            <Link
              to="/upload_document"
              className="text-blue-800 hover:text-pink-700 font-medium"
            >
              UploadDocument
            </Link>

            {/* Logout Button */}
            {/* <button
              onClick={handleLogout}
              className="text-blue-800 hover:text-pink-700 font-medium"
            >
              Logout
            </button> */}
      
        
      </div>
    </nav>
  );
}

export default Navbar;