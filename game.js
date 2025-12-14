// 游戏配置
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: 'game',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 300 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

// 游戏全局变量
let game;
let currentCharacter = 'cat';
let currentLanguage = 'zh';
let currentLevel = 1;
let isGameStarted = false;

// 游戏场景变量
let player;
let platforms;
let stars;
let bombs;
let cursors;
let score = 0;
let lives = 3;
let gameOver = false;
let scoreText;
let levelText;
let livesText;

// 语言文本
const lang = {
    zh: {
        startGame: '开始游戏',
        selectCharacter: '选择角色',
        settings: '设置',
        back: '返回',
        level: '关卡',
        collect: '收集',
        time: '时间',
        lives: '生命',
        jump: '跳跃',
        nextLevel: '下一关',
        gameOver: '游戏结束',
        congratulations: '恭喜通关！',
        tryAgain: '再试一次'
    },
    en: {
        startGame: 'Start Game',
        selectCharacter: 'Select Character',
        settings: 'Settings',
        back: 'Back',
        level: 'Level',
        collect: 'Collect',
        time: 'Time',
        lives: 'Lives',
        jump: 'Jump',
        nextLevel: 'Next Level',
        gameOver: 'Game Over',
        congratulations: 'Congratulations!',
        tryAgain: 'Try Again'
    }
};

// 角色表情
const characters = {
    cat: '🐱',
    dog: '🐶',
    rabbit: '🐰',
    bear: '🐻'
};

// 初始化游戏
function initGame() {
    // 菜单交互
    document.getElementById('start-game').addEventListener('click', startGame);
    document.getElementById('character-select-btn').addEventListener('click', showCharacterMenu);
    document.getElementById('settings').addEventListener('click', showSettingsMenu);
    document.getElementById('back-to-main').addEventListener('click', showMainMenu);
    document.getElementById('back-to-main-from-settings').addEventListener('click', showMainMenu);
    
    // 角色选择
    document.querySelectorAll('.character-option').forEach(option => {
        option.addEventListener('click', () => {
            document.querySelectorAll('.character-option').forEach(opt => opt.classList.remove('selected'));
            option.classList.add('selected');
            currentCharacter = option.dataset.character;
        });
    });
    
    // 语言选择
    document.querySelectorAll('.language-button').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.language-button').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            currentLanguage = btn.dataset.lang;
            updateLanguage();
        });
    });
    
    // 默认选择第一个角色
    document.querySelector('.character-option').classList.add('selected');
}

// 更新语言
function updateLanguage() {
    document.getElementById('start-game').textContent = lang[currentLanguage].startGame;
    document.getElementById('character-select-btn').textContent = lang[currentLanguage].selectCharacter;
    document.getElementById('settings').textContent = lang[currentLanguage].settings;
    document.getElementById('back-to-main').textContent = lang[currentLanguage].back;
    document.getElementById('back-to-main-from-settings').textContent = lang[currentLanguage].back;
    
    // 更新标题
    document.querySelector('#character-menu .menu-title').textContent = currentLanguage === 'zh' ? '选择你的角色' : 'Select Your Character';
    document.querySelector('#settings-menu .menu-title').textContent = currentLanguage === 'zh' ? '设置' : 'Settings';
}

// 显示主菜单
function showMainMenu() {
    document.getElementById('main-menu').style.display = 'flex';
    document.getElementById('character-menu').style.display = 'none';
    document.getElementById('settings-menu').style.display = 'none';
}

// 显示角色选择菜单
function showCharacterMenu() {
    document.getElementById('main-menu').style.display = 'none';
    document.getElementById('character-menu').style.display = 'flex';
    document.getElementById('settings-menu').style.display = 'none';
}

// 显示设置菜单
function showSettingsMenu() {
    document.getElementById('main-menu').style.display = 'none';
    document.getElementById('character-menu').style.display = 'none';
    document.getElementById('settings-menu').style.display = 'flex';
}

// 开始游戏
function startGame() {
    document.getElementById('main-menu').style.display = 'none';
    
    // 显示出发提示
    const gameContainer = document.getElementById('game-container');
    const startPrompt = document.createElement('div');
    startPrompt.textContent = '出发咯!';
    startPrompt.style.cssText = `
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 64px;
        color: #ff6b6b;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        z-index: 20;
        animation: fadeOut 2s ease-in-out;
    `;
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeOut {
            0% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            70% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
            100% { opacity: 0; transform: translate(-50%, -50%) scale(1); }
        }
    `;
    document.head.appendChild(style);
    gameContainer.appendChild(startPrompt);
    
    // 延迟启动游戏
    setTimeout(() => {
        if (!isGameStarted) {
            game = new Phaser.Game(config);
            isGameStarted = true;
        }
        gameContainer.removeChild(startPrompt);
    }, 2000);
}

// 游戏场景 - 预加载
function preload() {
    // 加载游戏资源
    this.load.image('sky', 'https://labs.phaser.io/assets/skies/space3.png');
    this.load.image('ground', 'https://labs.phaser.io/assets/platform.png');
    this.load.image('star', 'https://labs.phaser.io/assets/items/star.png');
    this.load.image('bomb', 'https://labs.phaser.io/assets/bombs/bomb.png');
    this.load.spritesheet('dude', 'https://labs.phaser.io/assets/sprites/dude.png', {
        frameWidth: 32,
        frameHeight: 48
    });
}

// 游戏场景 - 创建
function create() {
    // 创建背景
    this.add.image(400, 300, 'sky');
    
    // 创建平台组
    platforms = this.physics.add.staticGroup();
    
    // 创建地面和平台
    platforms.create(400, 568, 'ground').setScale(2).refreshBody();
    
    // 根据关卡创建不同的平台布局
    createLevelLayout(platforms, currentLevel);
    
    // 创建玩家
    player = this.physics.add.sprite(100, 450, 'dude');
    player.setBounce(0.2);
    player.setCollideWorldBounds(true);
    
    // 玩家动画
    this.anims.create({
        key: 'left',
        frames: this.anims.generateFrameNumbers('dude', { start: 0, end: 3 }),
        frameRate: 10,
        repeat: -1
    });
    
    this.anims.create({
        key: 'turn',
        frames: [{ key: 'dude', frame: 4 }],
        frameRate: 20
    });
    
    this.anims.create({
        key: 'right',
        frames: this.anims.generateFrameNumbers('dude', { start: 5, end: 8 }),
        frameRate: 10,
        repeat: -1
    });
    
    // 键盘控制
    cursors = this.input.keyboard.createCursorKeys();
    
    // 创建星星组
    stars = this.physics.add.group({
        key: 'star',
        repeat: 11,
        setXY: { x: 12, y: 0, stepX: 70 }
    });
    
    stars.children.iterate(function (child) {
        child.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));
    });
    
    // 创建炸弹组
    bombs = this.physics.add.group();
    
    // 分数文本
    scoreText = this.add.text(16, 16, `${lang[currentLanguage].collect}: 0`, { fontSize: '32px', fill: '#000' });
    levelText = this.add.text(300, 16, `${lang[currentLanguage].level}: ${currentLevel}`, { fontSize: '32px', fill: '#000' });
    livesText = this.add.text(600, 16, `${lang[currentLanguage].lives}: 3`, { fontSize: '32px', fill: '#000' });
    
    // 碰撞检测
    this.physics.add.collider(player, platforms);
    this.physics.add.collider(stars, platforms);
    this.physics.add.collider(bombs, platforms);
    
    // 重叠检测
    this.physics.add.overlap(player, stars, collectStar, null, this);
    this.physics.add.collider(player, bombs, hitBomb, null, this);
    
    // 初始化游戏状态
    score = 0;
    lives = 3;
    gameOver = false;
    
    // 添加场景方法
    this.showNextLevel = showNextLevel;
    this.showGameOver = showGameOver;
    this.showGameComplete = showGameComplete;
}

// 创建关卡布局
function createLevelLayout(platforms, level) {
    const layouts = {
        1: [
            { x: 400, y: 400, scale: 1 },
            { x: 600, y: 300, scale: 0.5 },
            { x: 50, y: 250, scale: 0.5 },
            { x: 750, y: 220, scale: 0.5 }
        ],
        2: [
            { x: 200, y: 400, scale: 0.5 },
            { x: 600, y: 400, scale: 0.5 },
            { x: 100, y: 300, scale: 0.5 },
            { x: 700, y: 300, scale: 0.5 },
            { x: 400, y: 200, scale: 0.5 }
        ],
        3: [
            { x: 150, y: 450, scale: 0.5 },
            { x: 300, y: 380, scale: 0.5 },
            { x: 450, y: 310, scale: 0.5 },
            { x: 600, y: 240, scale: 0.5 },
            { x: 750, y: 170, scale: 0.5 }
        ],
        4: [
            { x: 100, y: 400, scale: 0.5 },
            { x: 300, y: 350, scale: 0.5 },
            { x: 500, y: 300, scale: 0.5 },
            { x: 700, y: 250, scale: 0.5 },
            { x: 400, y: 150, scale: 0.5 },
            { x: 200, y: 100, scale: 0.5 }
        ],
        5: [
            { x: 50, y: 400, scale: 0.5 },
            { x: 200, y: 320, scale: 0.5 },
            { x: 350, y: 240, scale: 0.5 },
            { x: 500, y: 160, scale: 0.5 },
            { x: 650, y: 80, scale: 0.5 },
            { x: 750, y: 400, scale: 0.5 },
            { x: 400, y: 450, scale: 0.5 }
        ]
    };
    
    layouts[level].forEach(platform => {
        platforms.create(platform.x, platform.y, 'ground').setScale(platform.scale).refreshBody();
    });
}

// 收集星星
function collectStar(player, star) {
    star.disableBody(true, true);
    
    score += 10;
    scoreText.setText(`${lang[currentLanguage].collect}: ${score}`);
    
    // 生成新的星星
    if (stars.countActive(true) === 0) {
        // 所有星星收集完毕，进入下一关
        currentLevel++;
        
        if (currentLevel > 5) {
            // 游戏通关
            this.showGameComplete();
        } else {
            // 进入下一关
            this.showNextLevel();
        }
    }
    
    // 生成炸弹
    const x = (player.x < 400) ? Phaser.Math.Between(400, 800) : Phaser.Math.Between(0, 400);
    const bomb = bombs.create(x, 16, 'bomb');
    bomb.setBounce(1);
    bomb.setCollideWorldBounds(true);
    bomb.setVelocity(Phaser.Math.Between(-200, 200), 20);
}

// 碰到炸弹
function hitBomb(player, bomb) {
    this.physics.pause();
    
    player.setTint(0xff0000);
    player.anims.play('turn');
    
    lives--;
    livesText.setText(`${lang[currentLanguage].lives}: ${lives}`);
    
    if (lives <= 0) {
        gameOver = true;
        this.showGameOver();
    } else {
        // 重置玩家位置
        setTimeout(() => {
            player.clearTint();
            player.setPosition(100, 450);
            this.physics.resume();
        }, 1000);
    }
}

// 游戏场景 - 更新
function update() {
    if (gameOver) {
        return;
    }
    
    if (cursors.left.isDown) {
        player.setVelocityX(-160);
        player.anims.play('left', true);
    } else if (cursors.right.isDown) {
        player.setVelocityX(160);
        player.anims.play('right', true);
    } else {
        player.setVelocityX(0);
        player.anims.play('turn');
    }
    
    if (cursors.up.isDown && player.body.touching.down) {
        player.setVelocityY(-330);
    }
}



// 显示下一关提示
function showNextLevel() {
    this.physics.pause();
    
    const nextLevelText = this.add.text(400, 300, `${lang[currentLanguage].nextLevel} ${currentLevel}`, {
        fontSize: '48px',
        fill: '#000',
        backgroundColor: '#fff',
        padding: { x: 20, y: 10 }
    });
    nextLevelText.setOrigin(0.5);
    
    setTimeout(() => {
        this.scene.restart();
    }, 2000);
}

// 显示游戏结束
function showGameOver() {
    this.add.text(400, 300, lang[currentLanguage].gameOver, {
        fontSize: '64px',
        fill: '#ff0000',
        backgroundColor: '#fff',
        padding: { x: 20, y: 10 }
    }).setOrigin(0.5);
    
    this.add.text(400, 400, lang[currentLanguage].tryAgain, {
        fontSize: '32px',
        fill: '#000',
        backgroundColor: '#fff',
        padding: { x: 20, y: 10 }
    }).setOrigin(0.5).setInteractive()
      .on('pointerdown', () => {
          // 重置所有游戏状态
          currentLevel = 1;
          score = 0;
          lives = 3;
          gameOver = false;
          isGameStarted = false;
          
          // 重新启动游戏
          this.scene.restart();
      });
}

// 显示游戏完成
function showGameComplete() {
    this.add.text(400, 300, lang[currentLanguage].congratulations, {
        fontSize: '64px',
        fill: '#00ff00',
        backgroundColor: '#fff',
        padding: { x: 20, y: 10 }
    }).setOrigin(0.5);
    
    this.add.text(400, 400, lang[currentLanguage].tryAgain, {
        fontSize: '32px',
        fill: '#000',
        backgroundColor: '#fff',
        padding: { x: 20, y: 10 }
    }).setOrigin(0.5).setInteractive()
      .on('pointerdown', () => {
          // 重置所有游戏状态
          currentLevel = 1;
          score = 0;
          lives = 3;
          gameOver = false;
          isGameStarted = false;
          
          // 重新启动游戏
          this.scene.restart();
      });
}

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', initGame);