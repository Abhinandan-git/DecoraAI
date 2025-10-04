"use client";

import { useState } from "react";
import { FaRegEnvelope } from "react-icons/fa";
import { MdLockOutline } from "react-icons/md";

const AuthPage = () => {
	const [error, setError] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setEmail(event.target.value);
	};

	const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setPassword(event.target.value);
	};

	const handleLoginSubmit = async () => {
		const login_endpoint = process.env.NEXT_PUBLIC_SERVER_URL + "/auth/login";

		const response = await fetch(login_endpoint, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({
				email: email,
				password: password
			})
		});

		if (!response.ok) {
			setError(response.statusText);
			return;
		}
	};

	return (
		<main className="flex flex-col items-center justify-center min-h-screen py-2 bg-gray-100">
			<div className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
				<div className="bg-white rounded-2xl shadow-2xl flex w-2/3 max-w-4xl">
					<div className="w-3/5 p-5">
						<div className="text-left font-bold">
							<span className="text-blue-500">Decora</span>AI
						</div>
						<div className="py-10">
							<h2 className="text-3xl font-bold text-blue-500 mb-2">
								Sign in to your Account
							</h2>
							<div className="border-2 w-10 border-blue-500 inline-block mb-2"></div>
							<p className="text-gray-400 my-3">Use your email account</p>
							<div className="flex flex-col items-center gap-2">
								<div className="bg-gray-100 w-64 p-2 flex items-center">
									<FaRegEnvelope className="text-gray-400 m-2" />
									<input
										onChange={(event: React.ChangeEvent<HTMLInputElement>) => handleEmailChange(event)}
										value={email}
										type="email"
										name="email"
										placeholder="Email"
										className="bg-gray-100 outline-none text-sm flex-1"
									/>
								</div>
								<div className="bg-gray-100 w-64 p-2 flex items-center">
									<MdLockOutline className="text-gray-400 m-2" />
									<input
										onChange={(event: React.ChangeEvent<HTMLInputElement>) => handlePasswordChange(event)}
										value={password}
										type="password"
										name="password"
										placeholder="Password"
										className="bg-gray-100 outline-none text-sm flex-1"
									/>
								</div>
								<div className="flex justify-between w-64 mb-5">
									<label className="flex items-center text-xs">
										<a href="#" className="text-xs">Forgot Password?</a>
									</label>
								</div>
								<button
									className="border-2 border-blue-500 text-blue-500 rounded-full px-12 py-2 inline-block font-semibold hover:bg-blue-500 hover:text-white"
									onClick={async () => handleLoginSubmit()}
								>
									Sign In
								</button>
							</div>
						</div>
					</div>
					{/* Sign in section */}
					<div className="w-2/5 bg-blue-500 text-white rounded-tr-2xl rounded-br-2xl py-36 px-12">
						<h2 className="text-3xl font-bold mb-2">Hello, Friend!</h2>
						<div className="border-2 w-10 border-white inline-block mb-2"></div>
						<p className="mb-10">
							Fill up personal information and start your journey with us.
						</p>
						<a
							href="#"
							className="border-2 border-white rounded-full px-12 py-2 inline-block font-semibold hover:bg-white hover:text-blue-500"
						>
							Sign Up
						</a>
					</div>
				</div>
			</div >
		</main >
	)
}

export default AuthPage