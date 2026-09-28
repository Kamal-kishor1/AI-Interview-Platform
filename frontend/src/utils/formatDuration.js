export function formatDuration(seconds) {
    if (
        seconds === null ||
        seconds === undefined ||
        Number.isNaN(Number(seconds))
    ){
        return "N/A"
    }

    const totalSeconds = Math.max(0, Math.floor(Number(seconds)))

    const hours = Math.floor(totalSeconds / 3600)
    const minutes = Math.floor((totalSeconds % 3600) /60)
    const remainingSeconds = totalSeconds % 60

    if (hours > 0) {
        return `${hours} hr ${minutes} min ${remainingSeconds} sec`
    }

    if (minutes >0) {
        return `${minutes} min ${remainingSeconds} sec`
    }

    return `${remainingSeconds} sec`
}
