const BASE_URL = "http://127.0.0.1:5000";

export async function analyzeSingle(text) {
    const res = await fetch(`${BASE_URL}/analyze/single`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Analysis failed");
    return data;
}

export async function getDashboardStats() {
    const res = await fetch(`${BASE_URL}/dashboard/stats`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load dashboard");
    return data;
}

export async function getRecentAnalyses() {
    const res = await fetch(`${BASE_URL}/dashboard/recent`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load recent analyses");
    return data;
}

export async function analyzeBulk(file) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${BASE_URL}/analyze/bulk`, {
        method: "POST",
        body: formData
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Bulk upload failed");
    return data;
}

export async function getBulkResults(batchId) {
    const res = await fetch(`${BASE_URL}/analyze/bulk/${batchId}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load batch results");
    return data;
}