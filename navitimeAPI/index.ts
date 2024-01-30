import axios from "axios";
import dotenv from "dotenv";

type position = [number, number];

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const fetchData = async (start: position, goal: position) => {
  const getkey = dotenv.config().parsed?.X_RAPIDAPI_KEY;
  if (!getkey) {
    throw new Error("RAPIDAPI_KEY is not defined");
  }

  const options = {
    method: "GET",
    url: "https://navitime-route-totalnavi.p.rapidapi.com/route_transit",
    params: {
      start: String(start),
      goal: String(goal),
      start_time: "2020-08-19T14:00:00",
      datum: "wgs84",
      term: "1440",
      limit: "5",
      coord_unit: "degree",
    },
    headers: {
      "X-RapidAPI-Key": getkey,
      "X-RapidAPI-Host": "navitime-route-totalnavi.p.rapidapi.com",
    },
  };

  let times: number[] = [];
  try {
    const response = await axios.request(options);
    await delay(5000);
    //console.log(response.data);
    if (response.data.items?.length > 0) {
      for (let i = 0; i < response.data.items.length; i++) {
        const time = response.data.items[i].summary?.move?.time;
        if (time) {
          times.push(time);
        }
      }
    }
    times.sort();
    return times[0];
  } catch (error) {
    console.error(error);
  }
};

const rankCity = [
  "東京駅",
  "秋葉原",
  "銀座",
  "築地",
  "原宿",
  "渋谷",
  "六本木",
  "新宿",
  "恵比寿",
  "池袋",
  "上野",
  "浅草",
  "両国",
  "新橋",
  "品川",
  "蒲田",
  "お台場",
  "吉祥寺",
  "立川",
  "八王子",
];

const positions: position[] = [
  [35.68163907963647, 139.7657001031219],
  [35.698439821098894, 139.77301125877509],
  [35.674505397087614, 139.7669431877441],
  [35.6649328878006, 139.76686185059648],
  [35.67023026820395, 139.70246911914273],
  [35.659175829860466, 139.70127101649635],
  [35.66435153875589, 139.7320210238964],
  [35.689863293943056, 139.70062963980868],
  [35.646976027949265, 139.71012471225382],
  [35.7297030903869, 139.7109430122566],
  [35.71434139552781, 139.77745201225616],
  [35.71122361963859, 139.79766017596262],
  [35.69636369770102, 139.79272496432068],
  [35.666448703517396, 139.75831833923968],
  [35.628741608158826, 139.738824069925],
  [35.56261901579746, 139.71606236807213],
  [35.63030762753936, 139.77885454301236],
  [35.70339680206735, 139.5797926066491],
  [35.69813219564384, 139.41364423739006],
  [35.65579874099708, 139.33885289691088],
];

//console.log(rankCity.length);
//console.log(positions.length);
//const MAX = 2;
const MAX = rankCity.length;

const matrix: number[][] = [];
const main = async () => {
  for (let i = 0; i < MAX; i++) {
    const tmp: number[] = [];
    for (let j = 0; j < MAX; j++) {
      let t: number | undefined = 0;
      if (j < i) {
        t = matrix[j][i];
      } else if (i == j) {
        t = 0;
      } else {
        t = await fetchData(positions[i], positions[j]);
      }
      if (t != undefined) {
        console.log(rankCity[i] + " to " + rankCity[j] + ": " + t);
        tmp.push(t);
      } else {
        console.log(t);
        throw new Error("time is undefined");
      }
    }
    matrix.push(tmp);
  }
  console.log("[");
  for (let i = 0; i < MAX; i++) {
    console.log(matrix[i], ",");
  }
  console.log("]");
};
main();
