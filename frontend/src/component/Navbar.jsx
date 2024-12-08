import React from "react";

const Navbar = () => {
  return (
    <nav className="bg-blue-600 p-4">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo */}
        <div className="text-white text-lg font-bold">LWS Landslide warning system</div>

        {/* Hamburger Menu (Mobile) */}
        <div className="md:hidden">
          <button
            className="text-white focus:outline-none"
            onClick={() => {
              const menu = document.getElementById("mobile-menu");
              menu.classList.toggle("hidden");
            }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="1.5"
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M3.75 5.25h16.5m-16.5 7.5h16.5m-16.5 7.5h16.5"
              />
            </svg>
          </button>
        </div>

        {/* Menu (Desktop & Mobile) */}
        <div
          id="mobile-menu"
          className="hidden md:flex md:space-x-6 md:items-center"
        >
          <a
            href="#"
            className="block text-white hover:text-gray-200 transition"
          >
            Home
          </a>
          <a
            href="#"
            className="block text-white hover:text-gray-200 transition"
          >
            About
          </a>
          <a
            href="#"
            className="block text-white hover:text-gray-200 transition"
          >
            Services
          </a>
          <a
            href="#"
            className="block text-white hover:text-gray-200 transition"
          >
            Contact
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
