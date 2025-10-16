"use client";

import { HouseHeart, Plus } from "lucide-react";
import { getCookie } from "cookies-next/client";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { AiOutlineLoading } from "react-icons/ai";

const Dashboard = () => {
	const [loader, setLoader] = useState(false);

	useEffect(() => {
		setTimeout(() => {
			const access_token = getCookie("access_token");
			if (!access_token) {
				push("/auth");
			}
		}, 2);
	});

	const { push } = useRouter();

	const createNewCanvas = async () => {
		setLoader(true);

		const access_token = getCookie("access_token");
		try {
			const response = await fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/canvas/create", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"Authorization": "Bearer " + access_token
				}
			});
			const responseJson = await response.json();

			push("/editor/" + responseJson?.canvas_id);
		} catch (err) {
      console.log(err);
			throw Error();
		} finally {
			setLoader(false);
		}
	};

	return (
		<div className="min-h-screen bg-gray-100">
			<header className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
				<div className="flex items-center gap-3">
					<div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#ff4b2b] to-[#ff416c] flex items-center justify-center">
						<HouseHeart className="w-6 h-6 text-gray-100" />
					</div>
					<h1 className="text-xl font-semibold"><span className="bg-gradient-to-r from-[#ff4b2b] to-[#ff416c] inline-block text-transparent bg-clip-text">Decora</span>AI</h1>
				</div>
				<div className="w-3xs h-6 flex justify-between gap-2">
					<button className="transition-all w-1/3 h-8 font-medium rounded-md bg-gradient-to-br hover:from-[#ff4b2b] hover:to-[#ff416c] hover:text-gray-100">Editor</button>
					<button className="transition-all w-1/3 h-8 font-medium rounded-md bg-gradient-to-br hover:from-[#ff4b2b] hover:to-[#ff416c] hover:text-gray-100">Login</button>
					<button className="transition-all w-1/3 h-8 font-medium rounded-md bg-gradient-to-br hover:from-[#ff4b2b] hover:to-[#ff416c] hover:text-gray-100">Register</button>
				</div>
			</header>
			<main className="max-w-7xl mx-auto px-6 py-8">
				<div className="flex items-center justify-between mb-6">
					<h2 className="text-2xl font-normal text-[#1a1a1a]">Your Projects</h2>
				</div>
				<div onClick={() => createNewCanvas()} className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
					<div className="group cursor-pointer transition-all duration-300 rounded-2xl shadow-lg overflow-hidden">
						<div className="aspect-[1/1] p-6 flex flex-col">
							<div className="relative flex-1 flex items-center justify-center">
								<div className="absolute flex-1 flex items-center justify-center rounded-lg w-[100%] h-[100%] transition-all duration-300 bg-gradient-to-br from-[#ff4b2b] to-[#ff416c] opacity-0 group-hover:opacity-100 group-hover:scale-105"></div>
								{!loader ? <Plus className="w-10 h-10 z-0 text-[#1a1a1a] transition-all group-hover:text-white" /> : <AiOutlineLoading className="animate-spin text-[#1a1a1a] group-hover:text-white" />}
							</div>
						</div>
						<div className="pb-4 space-y-1 transition-all group-hover:scale-105">
							<h3 className="font-medium text-[#1a1a1a] text-center">Create New</h3>
						</div>
					</div>
				</div>
			</main>
		</div>
	);
};

export default Dashboard;
