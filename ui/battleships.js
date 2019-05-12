TEAMS_URL = "http://0.0.0.0:5678/bot_names/"
GAME_URL = "http://0.0.0.0:5678/play_game"

players = ['#playerOne', '#playerTwo'].map(function(id) {
  return new Vue({
    el: id,
    data: {
      teams: ["Loading..."],
      selectedTeam: "Loading...",
      board: []
    },
    beforeMount() {
      this.board = buildBoard()
    },
    mounted() {
      axios
        .get(TEAMS_URL)
        .then(response => {
          this.teams = response.data
          this.selectedTeam = null
        })
        .catch(error => {
          console.log(error)
          this.teams = ["Error loading team"]
          this.selectedTeam = "Error loading team"
        })
    }
  })
})

function clearBoards() {
  players.forEach(clearBoard)
}

function clearBoard(player) {
  player.board = buildBoard()
}

function buildBoard() {
  newBoard = []
  for (y = 0;y < 10;y++) {
    newRow = []
    for (x = 0;x < 10;x++) {
      newRow.push('w')
    }
    newBoard.push(newRow)
  }
  return newBoard;
}

function playNext(game, shotNum, animate, applyToOther=false, winner=null, maxShot=null) {
  if(!maxShot) {
      maxShot = game.reduce((t, c) => t + c.length, 0)
  }

  do {
    firingPlayerIndex = getFiringPlayerIndex(shotNum)
    if (applyToOther)
      receivingPlayerIndex = getReceivingPlayerIndex(shotNum)
    else
      receivingPlayerIndex = firingPlayerIndex
    shotIndex = getShotIndex(shotNum)

    player = getPlayer(receivingPlayerIndex)
    nextShot = getShot(game, firingPlayerIndex, shotIndex)
    
    row = player.board[nextShot.y]
    row[nextShot.x] = nextShot.state
    
    player.$set(player.board, nextShot.y, row)
  } while(++shotNum < maxShot && !animate)

	if (shotNum < maxShot && animate) {
		setTimeout(function(){ playNext(game, shotNum, animate, applyToOther, winner, maxShot) }, 100)
	}

  if (shotNum === maxShot && winner) {
    showWinner(winner)
  }
}

function getFiringPlayerIndex(shotNum) {
  return shotNum % 2
}

function getReceivingPlayerIndex(shotNum) {
  return (shotNum + 1) % 2
}

function getShotIndex(shotNum) {
  return Math.floor(shotNum / 2)
}

function getPlayer(playerIndex) {
  return players[playerIndex]
}

function getShot(game, playerIndex, shotIndex) {
  return game[playerIndex][shotIndex]
}

function showWinner(winner) {
  $('#bannerTitle').text(winner + " win!")
  $('#bannerDisplay').modal()
  closeBanner(3)
}

function showCommenceFiring(callback) {
  $('#bannerTitle').text("Commence Firing")
  $('#bannerDisplay').modal()
  closeBanner(3, callback)
}

function closeBanner(count, callback=null) {
  if (count === 0) {
    $('#bannerDisplay').modal('hide')
    if (callback) {
      callback()
    }
  } else {
    $('#bannerClose').text(count + "...")
    setTimeout(function(){ closeBanner(--count, callback) }, 1000)
  }
}

function playGame() {
  clearBoards()
  playerOne = players[0].selectedTeam
  playerTwo = players[1].selectedTeam
  showCommenceFiring(function() {
    axios
      .get(`${GAME_URL}/${playerOne}/${playerTwo}`)
      .then(response => {
        playNext(response.data.game.ships, 0, false)
        winner = response.data.game.winner
        setTimeout(function(){ playNext(response.data.game.shots, 0, true, true, winner) }, 100)
      })
      .catch(error => {
        console.log(error)
        alert("AVAST YE! " + error)
        this.errored = true
      })  
  })
}
