async function fetch_csv() {
    try {
        const response = await fetch('../static/final_merged.csv');
        const csvData = await response.text();
        return csvData;
    } catch (error) {
        console.error('Failed to load data.csv', error);
        throw error;
    }
}

export { fetch_csv }