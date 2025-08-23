class MosaicArtGame {
    constructor() {
        this.board = [];
        this.solution = [];
        this.size = 5;
        this.gameStarted = false;
        this.startTime = null;
        this.timerInterval = null;
        this.completed = false;
        
        this.initializeElements();
        this.bindEvents();
        this.startNewGame();
    }
    
    initializeElements() {
        this.gameBoard = document.getElementById('gameBoard');
        this.timerElement = document.getElementById('timer');
        this.progressElement = document.getElementById('progress');
        this.newGameBtn = document.getElementById('newGameBtn');
        this.checkBtn = document.getElementById('checkBtn');
        this.solveBtn = document.getElementById('solveBtn');
        this.difficultySelect = document.getElementById('difficultySelect');
    }
    
    bindEvents() {
        this.newGameBtn.addEventListener('click', () => this.startNewGame());
        this.checkBtn.addEventListener('click', () => this.checkSolution());
        this.solveBtn.addEventListener('click', () => this.showSolution());
        this.difficultySelect.addEventListener('change', () => this.startNewGame());
    }
    
    startNewGame() {
        this.size = this.getDifficultySize();
        this.gameStarted = false;
        this.completed = false;
        this.stopTimer();
        this.createBoard();
        this.generatePuzzle();
        this.renderBoard();
        this.updateProgress();
    }
    
    getDifficultySize() {
        const difficulty = this.difficultySelect.value;
        switch(difficulty) {
            case 'easy': return 5;
            case 'medium': return 10;
            case 'hard': return 15;
            default: return 5;
        }
    }
    
    createBoard() {
        this.board = [];
        this.solution = [];
        
        for (let i = 0; i < this.size; i++) {
            this.board[i] = [];
            this.solution[i] = [];
            for (let j = 0; j < this.size; j++) {
                this.board[i][j] = {
                    filled: false,
                    flagged: false,
                    number: null
                };
                this.solution[i][j] = false;
            }
        }
    }
    
    generatePuzzle() {
        // ランダムなパターンを生成
        this.generateRandomPattern();
        
        // 数字のヒントを計算
        this.calculateHints();
    }
    
    generateRandomPattern() {
        // 30-70%のマスを塗りつぶす
        const fillPercentage = 0.3 + Math.random() * 0.4;
        const totalCells = this.size * this.size;
        const cellsToFill = Math.floor(totalCells * fillPercentage);
        
        let filledCount = 0;
        while (filledCount < cellsToFill) {
            const i = Math.floor(Math.random() * this.size);
            const j = Math.floor(Math.random() * this.size);
            
            if (!this.solution[i][j]) {
                this.solution[i][j] = true;
                filledCount++;
            }
        }
    }
    
    calculateHints() {
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                const count = this.countAdjacentFilled(i, j);
                this.board[i][j].number = count;
            }
        }
    }
    
    countAdjacentFilled(row, col) {
        let count = 0;
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                if (i === 0 && j === 0) continue;
                
                const newRow = row + i;
                const newCol = col + j;
                
                if (this.isValidPosition(newRow, newCol) && this.solution[newRow][newCol]) {
                    count++;
                }
            }
        }
        return count;
    }
    
    isValidPosition(row, col) {
        return row >= 0 && row < this.size && col >= 0 && col < this.size;
    }
    
    renderBoard() {
        this.gameBoard.innerHTML = '';
        this.gameBoard.style.gridTemplateColumns = `repeat(${this.size}, 30px)`;
        
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = i;
                cell.dataset.col = j;
                
                const cellData = this.board[i][j];
                
                if (cellData.number !== null) {
                    cell.textContent = cellData.number;
                    cell.classList.add('number');
                } else if (cellData.filled) {
                    cell.classList.add('filled');
                } else if (cellData.flagged) {
                    cell.classList.add('flagged');
                    cell.textContent = '🚩';
                }
                
                cell.addEventListener('click', (e) => this.handleCellClick(i, j, e));
                cell.addEventListener('contextmenu', (e) => this.handleCellRightClick(i, j, e));
                
                this.gameBoard.appendChild(cell);
            }
        }
    }
    
    handleCellClick(row, col, event) {
        event.preventDefault();
        
        if (!this.gameStarted) {
            this.startTimer();
            this.gameStarted = true;
        }
        
        if (this.completed) return;
        
        const cellData = this.board[row][col];
        
        // 数字のマスはクリックできない
        if (cellData.number !== null) return;
        
        // フラグが立っている場合は何もしない
        if (cellData.flagged) return;
        
        cellData.filled = !cellData.filled;
        this.renderBoard();
        this.updateProgress();
        
        if (this.checkWinCondition()) {
            this.handleWin();
        }
    }
    
    handleCellRightClick(row, col, event) {
        event.preventDefault();
        
        if (!this.gameStarted) {
            this.startTimer();
            this.gameStarted = true;
        }
        
        if (this.completed) return;
        
        const cellData = this.board[row][col];
        
        // 数字のマスはフラグを立てられない
        if (cellData.number !== null) return;
        
        // 塗りつぶされているマスはフラグを立てられない
        if (cellData.filled) return;
        
        cellData.flagged = !cellData.flagged;
        this.renderBoard();
    }
    
    checkWinCondition() {
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (this.solution[i][j] !== this.board[i][j].filled) {
                    return false;
                }
            }
        }
        return true;
    }
    
    handleWin() {
        this.completed = true;
        this.stopTimer();
        setTimeout(() => {
            alert('おめでとうございます！パズルが完成しました！');
        }, 100);
    }
    
    checkSolution() {
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                const cell = this.gameBoard.querySelector(`[data-row="${i}"][data-col="${j}"]`);
                const cellData = this.board[i][j];
                
                if (cellData.number === null) {
                    if (cellData.filled === this.solution[i][j]) {
                        cell.classList.add('correct');
                    } else if (cellData.filled) {
                        cell.classList.add('incorrect');
                    }
                }
            }
        }
        
        setTimeout(() => {
            this.renderBoard();
        }, 2000);
    }
    
    showSolution() {
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                this.board[i][j].filled = this.solution[i][j];
                this.board[i][j].flagged = false;
            }
        }
        this.renderBoard();
        this.updateProgress();
    }
    
    updateProgress() {
        let correctCount = 0;
        let totalCount = 0;
        
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (this.board[i][j].number === null) {
                    totalCount++;
                    if (this.board[i][j].filled === this.solution[i][j]) {
                        correctCount++;
                    }
                }
            }
        }
        
        const percentage = totalCount > 0 ? Math.round((correctCount / totalCount) * 100) : 0;
        this.progressElement.textContent = `${percentage}%`;
    }
    
    startTimer() {
        this.startTime = Date.now();
        this.timerInterval = setInterval(() => {
            const elapsed = Date.now() - this.startTime;
            const minutes = Math.floor(elapsed / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);
            this.timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }
    
    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }
}

// ゲームを初期化
document.addEventListener('DOMContentLoaded', () => {
    new MosaicArtGame();
});