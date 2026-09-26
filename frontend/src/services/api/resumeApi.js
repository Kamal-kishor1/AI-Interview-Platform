import api from "./axios";

export const uploadResume = async (file, name, email) => {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("name", name);
  formData.append("email", email);

  const response = await api.post(
    "/api/v1/resumes/upload",
    formData
  );

  return response.data;
};