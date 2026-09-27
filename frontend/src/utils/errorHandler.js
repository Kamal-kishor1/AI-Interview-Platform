export function getApiErrorMessage(
  error,
  fallbackMessage = "Something went wrong."
) {
  const detail = error?.response?.data?.detail;

  // FastAPI validation errors
  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => item?.msg)
      .filter(Boolean);

    if (messages.length > 0) {
      return messages.join(", ");
    }
  }

  // FastAPI HTTPException
  if (typeof detail === "string") {
    return detail;
  }

  // Network error
  if (!error?.response) {
    return "Unable to connect to the server.";
  }

  return fallbackMessage;
}