const date = new Date(2049, 1);

print(date);
JapaneseHoliday(date);

function JapaneseHoliday(date) {
    const year = date.getFullYear();
    holidayDate = theFisrtDayOfTheYear(year);
    holidayDate.push(comingOfAgeDay(year));
    holidayDate = nationalFoundationDay(year, holidayDate);
    holidayDate = emperorBirthday(year, holidayDate);
    holidayDate = vernalEquinoxDay_Holiday(year, holidayDate);
    holidayDate = showaDay(year, holidayDate);
    holidayDate = constitutionDayGreeneryDayChildrenDay(year, holidayDate);
    holidayDate.push(marinDay(year));
    holidayDate = mountainDay(year, holidayDate);
    holidayDate.push(respectForTheAgedDay(year));
    holidayDate = autumnalEquinoxDay_Holiday(year, holidayDate);
    holidayDate.push(sportsDay(year));
    holidayDate = cultureDay(year, holidayDate);
    holidayDate = laborThanksgivingDay(year, holidayDate);
    
    print(holidayDate);
}

function theFisrtDayOfTheYear(year){
    let holidayDate = [];
    // 元日の振替休日判定
    let theFisrtDayOfTheYear = new Date(year, 0, 1);
    if (theFisrtDayOfTheYear.getDay() == 0){
        theFisrtDayOfTheYear = new Date(year, 0, 2);
        holidayDate.push("1" + "-" + "1");
        holidayDate.push("1" + "-" + theFisrtDayOfTheYear.getDate());
    }else{
        holidayDate.push("1" + "-" + theFisrtDayOfTheYear.getDate());
    }
    return holidayDate;
}

function nationalFoundationDay(year, holiday){
    let nationalFoundationDay = new Date(year, 1, 11);
    // 建国記念日の振替休日判定
    if (nationalFoundationDay.getDay() == 0){
        nationalFoundationDay = new Date(year, 1, 12);
        holiday.push("2" + "-" + "11");
        holiday.push("2" + "-" + nationalFoundationDay.getDate());
    }else{
        holiday.push("2" + "-" + nationalFoundationDay.getDate());
    }

    return holiday;
}

function emperorBirthday(year, holiday){
    let emperorBirthday = new Date(year, 1, 23);
    // 天皇誕生日の振替休日判定
    if (emperorBirthday.getDay() == 0){
        emperorBirthday = new Date(year, 1, 24);
        holiday.push("2" + "-" + 23);
        holiday.push("2" + "-" + emperorBirthday.getDate());
    }else{
        holiday.push("2" + "-" + emperorBirthday.getDate());
    }

    return holiday;
}

function showaDay(year, holiday){
    let showaDay = new Date(year, 3, 29);
    // 昭和の日の振替休日判定
    if (showaDay.getDay() == 0){
        showaDay = new Date(year, 3, 30);
        holiday.push("4" + "-" + "29");
        holiday.push("4" + "-" + showaDay.getDate());
    }else{
        holiday.push("4" + "-" + showaDay.getDate());
    }
    
    return holiday;
}

function constitutionDayGreeneryDayChildrenDay(year, holiday){
    const constitutionDay = new Date(year, 4, 3);
    const greeneryDay = new Date(year, 4, 4);
    const childrensDay = new Date(year, 4, 5);

    // 憲法記念日～こどもの日までの振替判定
    if (constitutionDay.getDay() == 0 || greeneryDay.getDay() == 0 || childrensDay.getDay() == 0){
        holiday.push("5" + "-" + constitutionDay.getDate());
        holiday.push("5" + "-" + greeneryDay.getDate());
        holiday.push("5" + "-" + childrensDay.getDate());
        const transferDate = new Date(year, 4, 6);
        holiday.push("5" + "-" + transferDate.getDate());
    }else{
        holiday.push("5" + "-" + constitutionDay.getDate());
        holiday.push("5" + "-" + greeneryDay.getDate());
        holiday.push("5" + "-" + childrensDay.getDate());
    }

    return holiday
}

function mountainDay(year, holiday){
    let mountainDay = new Date(year, 7, 11);
    // 山の日の振替休日判定
    if (mountainDay.getDay() == 0){
        mountainDay = new Date(year, 7, 12);
        holiday.push("8" + "-" + "11");
        holiday.push("8" + "-" + mountainDay.getDate());
    }else{
        holiday.push("8" + "-" + mountainDay.getDate());
    }
    return holiday;
}

function cultureDay(year, holiday){
    let cultureDay = new Date(year, 10, 3);
    // 文化の日の振替休日判定
    if (cultureDay.getDay() == 0){
        cultureDay = new Date(year, 10, 4);
        holiday.push("11" + "-" + "3");
        holiday.push("11" + "-" + cultureDay.getDate());
    }else{
        holiday.push("11" + "-" + cultureDay.getDate());
    }
    return holiday;
}

function laborThanksgivingDay(year, holiday){
    let laborThanksgivingDay = new Date(year, 10, 23);
    // 勤労感謝の日の振替休日判定
    if (laborThanksgivingDay.getDay() == 0){
        laborThanksgivingDay = new Date(year, 10, 24);
        holiday.push("11" + "-" + "23");
        holiday.push("11" + "-" + laborThanksgivingDay.getDate());
    }else{
        holiday.push("11" + "-" + laborThanksgivingDay.getDate());
    }

    return holiday
}


// 成人の日
function comingOfAgeDay(year){
    /**
     * 成人の日は、1月の第2月曜日
    */
    // 1月1日の曜日を取得（日曜日：0 ～ 土曜日：6）
    const firstDay = new Date(year, 0, 1);

    // 第1月曜日に設定する処理
    let dayCounter = 0;
    if (firstDay.getDay() == 1){
        // 1月1日が月曜日の場合
        dayCounter = 0;
    }else if(firstDay.getDay() == 0){
        // 1月1日が日曜日の場合
        dayCounter = 1;
    }else if(2 <= firstDay.getDay() && firstDay.getDay() <= 6){
        // 1月1日が火～土曜日の場合
        // 土曜日までの差を導出
        dayCounter = (6 - Number(firstDay.getDay())); 
        // 第1月曜日までの差をたす
        dayCounter += 2;
    }

    const comingOfAgeDay = new Date(year, 0, (1 + dayCounter + 7));
    return "1" + "-" + comingOfAgeDay.getDate();
}

//海の日
function marinDay(year){
    /**
     * 海の日は、7月の第3月曜日
    */
    // 7月1日の曜日を取得（日曜日：0 ～ 土曜日：6）
    const firstDay = new Date(year, 6, 1);

    // 第1月曜日に設定する処理
    let dayCounter = 0;
    if (firstDay.getDay() == 1){
        // 7月1日が月曜日の場合
        dayCounter = 0;
    }else if(firstDay.getDay() == 0){
        // 7月1日が日曜日の場合
        dayCounter = 1;
    }else if(2 <= firstDay.getDay() && firstDay.getDay() <= 6){
        // 7月1日が火～土曜日の場合
        // 土曜日までの差を導出
        dayCounter = (6 - Number(firstDay.getDay())); 
        // 第1月曜日までの差をたす
        dayCounter += 2;
    }

    let marinDate = dayCounter + 15;

    const marinDay = new Date(year, 6, marinDate);
    return "7" + "-" + marinDay.getDate();
}

//敬老の日
function respectForTheAgedDay(year){
    /**
     * 敬老の日は、9月の第3月曜日
    */
    // 9月1日の曜日を取得（日曜日：0 ～ 土曜日：6）
    const firstDay = new Date(year, 8, 1);

    // 第1月曜日に設定する処理
    let dayCounter = 0;
    if (firstDay.getDay() == 1){
        // 9月1日が月曜日の場合
        dayCounter = 0;
    }else if(firstDay.getDay() == 0){
        // 9月1日が日曜日の場合
        dayCounter = 1;
    }else if(2 <= firstDay.getDay() && firstDay.getDay() <= 6){
        // 9月1日が火～土曜日の場合
        // 土曜日までの差を導出
        dayCounter = (6 - Number(firstDay.getDay())); 
        // 第1月曜日までの差をたす
        dayCounter += 2;
    }
    const respectForTheAgedDay = new Date(year, 8, (1 + dayCounter + 14));
    return "9" + "-" + respectForTheAgedDay.getDate();
}

//スポーツの日
function sportsDay(year){
    /**
     * スポーツの日は、10月の第2月曜日
    */
    // 10月1日の曜日を取得（日曜日：0 ～ 土曜日：6）
    const firstDay = new Date(year, 9, 1);

    // 第1月曜日に設定する処理
    let dayCounter = 0;
    if (firstDay.getDay() == 1){
        // 10月1日が月曜日の場合
        dayCounter = 0;
    }else if(firstDay.getDay() == 0){
        // 10月1日が日曜日の場合
        dayCounter = 1;
    }else if(2 <= firstDay.getDay() && firstDay.getDay() <= 6){
        // 10月1日が火～土曜日の場合
        // 土曜日までの差を導出
        dayCounter = (6 - Number(firstDay.getDay())); 
        // 第1月曜日までの差をたす
        dayCounter += 2;
    }

    const sportsDay = new Date(year, 9, (1 + dayCounter + 7));
    return "10" + "-" + sportsDay.getDate();
}

// 春分の日
function vernalEquinoxDay_Holiday(year, holiday){
    /**
     * 春分の日　計算
     * =int(20.8431+0.242194*(自分が調べたい年-1980))-int((自分が調べたい年-1980)/4)
     * 以下参考URL
     * https://dime.jp/genre/845341/#:~:text=%E3%81%BE%E3%81%9F%E3%80%81%E5%A4%A9%E6%96%87%E5%AD%A6%E3%81%A7%E3%81%84%E3%81%86%E3%81%A8%E3%81%93%E3%82%8D,%E3%81%AE%E6%97%A5%E3%81%AB%E3%81%AA%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82
    */
    const vernalEquinoxDay_cal = Math.trunc(20.8431+0.242194*(year-1980))-Math.trunc((year-1980)/4);
    let vernalEquinoxDay = new Date(year, 2, vernalEquinoxDay_cal);
    holiday.push("3" + "-" + vernalEquinoxDay.getDate());
    if(vernalEquinoxDay.getDay() == 0){
        vernalEquinoxDay = new Date(year, 2, vernalEquinoxDay_cal + 1);
        holiday.push("3" + "-" + vernalEquinoxDay.getDate());
    }

    return holiday;
}

// 秋分の日
function autumnalEquinoxDay_Holiday(year, holiday){
    /**
     * 秋分の日　計算
     * =int(23.2488+0.242194*(自分が調べたい年-1980))-int((自分が調べたい年-1980)/4);
    */
    const autumnalEquinoxDay_cal = Math.trunc(23.2488+0.242194*(year-1980))-Math.trunc((year-1980)/4);
    let autumnalEquinoxDay = new Date(year, 8, autumnalEquinoxDay_cal);

    let respectForTheAgedDay = holiday[holiday.length - 1];
    const respectForTheAgedDate = respectForTheAgedDay.split("-");
    
    // 国民の休日の計算

    if (nationalHoliday(respectForTheAgedDate[1], autumnalEquinoxDay.getDate())) {
        const nationalHoliday = Number(respectForTheAgedDate[1]) + 1;
        holiday.push("9" + "-" + nationalHoliday);
    }

    holiday.push("9" + "-" + autumnalEquinoxDay.getDate());

    if(autumnalEquinoxDay.getDay() == 0){
        autumnalEquinoxDay = new Date(year, 8, autumnalEquinoxDay_cal + 1);
        holiday.push("9" + "-" + autumnalEquinoxDay.getDate());
    }

    return holiday;
}

// 国民の祝日
function nationalHoliday(respectForTheAgedDay, autumnalEquinoxDay) {
    const nationalHoliday = Number(autumnalEquinoxDay) - Number(respectForTheAgedDay);
    if (nationalHoliday == 2) {
        return true;
    } else {
        return false;
    }
}
