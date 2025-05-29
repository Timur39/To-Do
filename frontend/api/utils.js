export async function operateData({
  url = "",
  method = "",
  data = {},
  isProtected = false,
  isForm = false,
}) {
  try {
    const params = {
      method: method,
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
    if (method === "GET") {
      delete params.body;
    }
    if (isForm) {
      params.headers = {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      };
      params.body = new URLSearchParams(data);
    }
    if (isProtected) {
      params.headers["Authorization"] = `Bearer ${localStorage.getItem(
        "accessToken"
      )}`;
    }
    const response = await fetch(url, params);

    return response;
  } catch {
    err;
  }
  {
    console.error("operateData error:", err);
  }
}
