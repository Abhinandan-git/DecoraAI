"use client";

import { useState } from "react";
import { FaRegEnvelope } from "react-icons/fa";
import { MdLockOutline } from "react-icons/md";

const DesignerLogin = () => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	
	const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setEmail(event.target.value);
	};
	
	const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setPassword(event.target.value);
	};
	
	return (
		<main className="flex flex-col items-center justify-center min-h-screen py-2 bg-gray-100">
			<div className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
				<div className="bg-white rounded-2xl shadow-2xl flex w-2/3 max-w-4xl">
					<div className="w-2/5 bg-green-500 text-white rounded-tl-2xl rounded-bl-2xl py-36 px-12">
						<h2 className="text-3xl font-bold mb-2">Hello, Friend!</h2>
						<div className="border-2 w-10 border-white inline-block mb-2"></div>
						<p className="mb-10">
							Fill up personal information and start your journey with us.
						</p>
						<a
							href="#"
							className="border-2 border-white rounded-full px-12 py-2 inline-block font-semibold hover:bg-white hover:text-green-500"
						>
							Sign Up
						</a>
					</div>
					{/* Sign in section */}
					<div className="w-3/5 p-5">
						<div className="text-right font-bold">
							<span className="text-green-500">Decora</span>AI
						</div>
						<div className="py-10">
							<h2 className="text-3xl font-bold text-green-500 mb-2">
								Sign in to your Account
							</h2>
							<div className="border-2 w-10 border-green-500 inline-block mb-2"></div>
							<p className="text-gray-400 my-3">Use your email account</p>
							<div className="flex flex-col items-center gap-2">
								<div className="bg-gray-100 w-64 p-2 flex items-center">
									<FaRegEnvelope className="text-gray-400 m-2" />
									<input
										onChange={(event: React.ChangeEvent<HTMLInputElement>) => handleEmailChange(event)}
										value={email}
										type="email"
										name="email"
										placeholder="Designer Email"
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
									className="border-2 border-green-500 text-green-500 rounded-full px-12 py-2 inline-block font-semibold hover:bg-green-500 hover:text-white"
								>
									Sign In
								</button>
							</div>
						</div>
					</div>
				</div>
			</div >
		</main >
	)
}

export default DesignerLogin