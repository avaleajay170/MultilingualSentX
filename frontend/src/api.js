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