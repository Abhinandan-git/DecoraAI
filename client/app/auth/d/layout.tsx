import type { Metadata } from "next";

export const metadata: Metadata = {
	title: "DecoraAI | Designer Login",
	description: "",
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en">
			<body
				data-new-gr-c-s-check-loaded="14.1255.0"
				data-gr-ext-installed=""
			>
				{children}
			</body>
		</html>
	);
}
