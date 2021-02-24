const today = new Date();
const this_year = today.getFullYear();

// start as this year's groundhog day (months 0-11)
var groundhog_day = new Date(this_year, 1, 2, 23, 59, 59);
// if its past, update the year by +1, otherwise does not change
groundhog_day.setFullYear(this_year + (groundhog_day.getTime() < today.getTime()));

// conversion factor from miliseconds to days
const conversion = 1000 * 3600 * 24;
// time remaining to the next groundhog day, in miliseconds
var remaining = groundhog_day.getTime() - today.getTime();
// show remaining time in days
console.log(`${Math.floor(remaining / conversion)} days remaining for Groundhog Day!`);