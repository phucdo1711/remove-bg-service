import Axios from "axios";
// import { BASE_URL } from "../config";
// import { API_URL } from "appConfig";

const axios = Axios.create({
  baseURL: '/',// 'http://localhost:5000' ,
  timeout: 60000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

export default axios;
