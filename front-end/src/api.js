let ip = 'http://34.245.151.229:5000'

//Mock
// let fetch = () => Promise.resolve({json:() =>Promise.resolve([
//     {
//         "airData": "0.9",
//         "date": "2018-03-08",
//         "lightData": "0.1",
//         "moistureData": "0.5",
//         "tempData": "24.5",
//         "time": "19:29:59"
//     },
//     {
//         "airData": "0.89",
//         "date": "2018-03-08",
//         "lightData": "0.09",
//         "moistureData": "0.49",
//         "tempData": "25.0",
//         "time": "19:30:19"
//     },
//     {
//         "airData": "0.91",
//         "date": "2018-03-08",
//         "lightData": "0.05",
//         "moistureData": "0.45",
//         "tempData": "25.5",
//         "time": "19:30:34"
//     },
//     {
//         "airData": "0.92",
//         "date": "2018-03-08",
//         "lightData": "0.06",
//         "moistureData": "0.41",
//         "tempData": "24.5",
//         "time": "19:30:50"
//     }
// ])})

export function getAll() {
    return fetch(ip+'/data')
    .then(res => res.json())
    .then(json => Promise.resolve({
        airData:json.map(d => d.airData),
        lightData:json.map(d => d.lightData),
        moistureData:json.map(d => d.moistureData),
        tempData:json.map(d => d.tempData),
        dateTime:json.map(d => new Date(d.date+'T'+d.time)),
    }))
}

export function getProcessedData() {
    return fetch(ip+'/processedData')
    .then(res => res.json())
}

//Min max temperature
//Wakeup time
//Desired sleeping amount
//

