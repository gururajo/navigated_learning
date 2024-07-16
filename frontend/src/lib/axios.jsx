import axios from "axios";
export const SERVERIP = "localhost:5000";
export const baseURL = "https://" + SERVERIP;

const api = axios.create({
	baseURL: baseURL,
	headers: {
		"Content-Type": "application/json",
		"Access-Control-Allow-Origin": "*", // Allow requests from any origin
	},
});

api.interceptors.request.use(
	(config) => {
		const token = localStorage.getItem("token");
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	(error) => Promise.reject(error)
);

api.interceptors.response.use(
	(response) => response,
	async (error) => {
		// If the error status is 401, it means the token has expired and we need to redirect to login
		if (error.response.status === 401) {
			// Redirect to login
			console.log(
				"Redirecting to the login page - Access Token expired !!"
			);
			window.location.href = "/login";
			return;
		}
		return Promise.reject(error);
	}
);

export default api;
