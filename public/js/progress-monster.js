let base_game_speed = 4

const debug_mode = true



let mons = [
    {name: "slime", max_hp: 3, hp: 3, dmg: 1},
    {name: "goblin", max_hp: 7, hp: 7, dmg: 3},
    {name: "human", max_hp: 20, hp: 20, dmg: 7},
    {name: "orc", max_hp: 45, hp: 45, dmg: 12},
    {name: "dragon", max_hp: 5000, hp: 5000, dmg: 300}
]

let skills = [
    {name:"endurance", bonus:{name: "max_hp"}, level: 0}
]

let char = {
    max_hp: 10,
    hp: 0,
    hp_regen: 0.01,
    strength: 0.03,
    dex: 0.03,
    max_mana: 1,
    mana: 0,
    mana_regen: 0.001,
}

let now_monster = null
let now_skill = null

document.addEventListener("DOMContentLoaded", () => {
    const tick_id = setInterval(tick, 1000/base_game_speed)
    load()

});


async function attack(){

}



async function regenerate(){
    if (char.hp < char.max_hp){
        char.hp = Math.round((char.hp + char.hp_regen)*10000)/10000
        if (char.hp > char.max_hp){
            char.hp = char.max_hp
        }

        if (char.hp < 1000){
            document.querySelector("#hp").innerHTML = `Health: ${char.hp}/${char.max_hp}`
        } else {
            document.querySelector("#hp").innerHTML = `Health: ${Math.round(char.hp)}/${Math.round(char.max_hp)}`
        }
    }

    
    

    if (char.mana < char.max_mana){
        char.mana = Math.round((char.mana + char.mana_regen)*10000)/10000
        if (char.mana > char.max_mana){
            char.mana = char.max_mana
        }
        
        if (char.hp < 1000){
            document.querySelector("#mana").innerHTML = `Mana: ${char.mana}/${char.max_mana}`
        } else {
            document.querySelector("#mana").innerHTML = `Mana: ${Math.round(char.mana)}/${Math.round(char.max_mana)}`
        }
    }

    document.querySelector("#mana").innerHTML = `Mana: ${char.mana}/${char.max_mana}`
}

async function train(){
    
}

function tick(){
    attack()
    regenerate()
    train()
}

function save(){

}

async function load(){
    for (let i = 0; i < mons.length - 1; i++){
        mon_div = document.createElement("div", id="mon_"+i)
        document.querySelector(".home").innerHTML += mon_div.innerHTML
        update_mon(i)
    }
}

function update_mon(mon_id){
    main = document.createElement("div")
    let father = document.querySelector("#mon_"+mon_id)
    let mon = mons[mon_id]
    father.innerHTML = `${mon.name}  ${mon.hp}/${mon.max_hp} hp and ${mon.dmg} attack`

}