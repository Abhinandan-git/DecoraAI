"use client";

import React, { useState } from "react";

export default function AuthPage() {
  const [signingIn, setSigningIn] = useState(true);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");

  const sendRequest = async (endpoint: string, body: object) => {
		await fetch(endpoint, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(body)
		}).catch((error: string) => {
      setError(error);
    });
  };

  const signupHandler = async () => {
    const endpoint = process.env.NEXT_PUBLIC_SERVER_URL + "/auth/register";
    const body = {
      username: name,
      email: email,
      password: password
    }

    await sendRequest(endpoint, body);
  };

  const signinHandler = async () => {
    const endpoint = process.env.NEXT_PUBLIC_SERVER_URL + "/auth/login";
    const body = {
      email: email,
      password: password
    }

    await sendRequest(endpoint, body);
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="relative w-[678px] max-w-full min-h-[400px] bg-white rounded-[10px] shadow-[0_14px_28px_rgba(0,0,0,0.25),_0_10px_10px_rgba(0,0,0,0.22)] overflow-hidden">
        {/* Sign Up Container */}
        {error}
        <div
          className={"absolute top-0 left-0 w-1/2 h-full transition-all duration-700 ease-in-out opacity-0 z-[1] " + (!signingIn && "translate-x-full opacity-100 z-[5]")}>
          <div className="bg-white flex flex-col items-center justify-center px-[50px] h-full text-center">
            <h1 className="font-bold m-0 text-2xl">Create Account</h1>
            <input
              type="text"
              placeholder="Name"
              className="bg-gray-200 border-none py-3 px-4 my-2 w-full focus:outline-none rounded-[4px]"
              value={name}
              onChange={(event: React.ChangeEvent<HTMLInputElement>) => setName(event.target.value)}
            />
            <input
              type="email"
              placeholder="Email"
              className="bg-gray-200 border-none py-3 px-4 my-2 w-full focus:outline-none rounded-[4px]"
              value={email}
              onChange={(event: React.ChangeEvent<HTMLInputElement>) => setEmail(event.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              className="bg-gray-200 border-none py-3 px-4 my-2 w-full focus:outline-none rounded-[4px]"
              value={password}
              onChange={(event: React.ChangeEvent<HTMLInputElement>) => setPassword(event.target.value)}
            />
            <button
              type="button"
              className="rounded-full border border-[#ff4b2b] bg-[#ff4b2b] text-white text-xs font-bold py-3 px-11 tracking-wider uppercase active:scale-95 transition-transform duration-100"
              onClick={async () => signupHandler()}
            >
              Sign Up
            </button>
          </div>
        </div>

        {/* Sign In Container */}
        <div
          className={"absolute top-0 left-0 w-1/2 h-full transition-all duration-700 ease-in-out z-[2] " + (!signingIn && "translate-x-full")}>
          <div className="bg-white flex flex-col items-center justify-center px-[50px] h-full text-center">
            <h1 className="font-bold m-0 text-2xl">Sign in</h1>
            <input
              type="email"
              placeholder="Email"
              className="bg-gray-200 border-none py-3 px-4 my-2 w-full focus:outline-none rounded-[4px]"
              value={email}
              onChange={(event: React.ChangeEvent<HTMLInputElement>) => setEmail(event.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              className="bg-gray-200 border-none py-3 px-4 my-2 w-full focus:outline-none rounded-[4px]"
              value={password}
              onChange={(event: React.ChangeEvent<HTMLInputElement>) => setPassword(event.target.value)}
            />
            <button
              type="button"
              className="rounded-full border border-[#ff4b2b] bg-[#ff4b2b] text-white text-xs font-bold py-3 px-11 tracking-wider uppercase active:scale-95 transition-transform duration-100 my-2"
              onClick={async () => signinHandler()}
            >
              Sign In
            </button>
          </div>
        </div>

        {/* Overlay Container */}
        <div
          className={"absolute top-0 left-1/2 w-1/2 h-full overflow-hidden transition-transform duration-700 ease-in-out z-[100] " + (!signingIn && "-translate-x-full")}>
          <div
            className={"bg-gradient-to-r from-[#ff4b2b] to-[#ff416c] bg-cover bg-no-repeat bg-left text-white relative left-[-100%] w-[200%] h-full transition-transform duration-700 ease-in-out " + (!signingIn && "translate-x-1/2")}>
            {/* Left Overlay Panel */}
            <div
              className={"absolute top-0 left-0 flex flex-col items-center justify-center px-10 text-center h-full w-1/2 transition-transform duration-700 ease-in-out " + (signingIn ? "-translate-x-1/5" : "translate-x-0")}>
              <h1 className="font-bold text-2xl">Welcome Back!</h1>
              <p className="text-sm font-light leading-5 tracking-wide my-5">
                To keep connected with us please login with your details
              </p>
              <button
                onClick={() => setSigningIn(true)}
                className="rounded-full border border-white bg-transparent text-white text-xs font-bold py-3 px-11 tracking-wider uppercase active:scale-95 transition-transform duration-100"
              >
                Sign In
              </button>
            </div>

            {/* Right Overlay Panel */}
            <div
              className={"absolute top-0 right-0 flex flex-col items-center justify-center px-10 text-center h-full w-1/2 transition-transform duration-700 ease-in-out " + (!signingIn ? "translate-x-[20%]" : "translate-x-0")}>
              <h1 className="font-bold text-2xl">Hello, Friend!</h1>
              <p className="text-sm font-light leading-5 tracking-wide my-5">
                Enter your details and start your journey with us
              </p>
              <button
                onClick={() => setSigningIn(false)}
                className="rounded-full border border-white bg-transparent text-white text-xs font-bold py-3 px-11 tracking-wider uppercase active:scale-95 transition-transform duration-100"
              >
                Sign Up
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
