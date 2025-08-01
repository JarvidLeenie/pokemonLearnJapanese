// Load the JSON data
let pokemonData = [];
let originsData = {};
let tcgTypesData = {};

// Global variables for mobile navigation
let navigateToCard = null;

// Mobile detection function - cached to prevent excessive calls
let mobileDetectionCache = null;
function isMobileDevice() {
    // Return cached result if available
    if (mobileDetectionCache !== null) {
        return mobileDetectionCache;
    }
    
    const width = window.innerWidth;
    const userAgent = navigator.userAgent;
    const orientation = window.orientation;
    
    const isMobile = width <= 768 || 
                     /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent) ||
                     (orientation !== undefined && orientation !== 0) ||
                     ('ontouchstart' in window);
    
    // Cache the result
    mobileDetectionCache = isMobile;
    
    // Debug logging (only once)
    console.log('Mobile detection:', {
        width,
        userAgent: userAgent.substring(0, 50) + '...',
        orientation,
        isMobile
    });
    
    return isMobile;
}

// Clear mobile detection cache on resize
window.addEventListener('resize', () => {
    mobileDetectionCache = null;
});

// Function to add furigana readings to kanji
function addFurigana(text) {
    // Simple kanji to reading mappings for common characters
    const kanjiReadings = {
        '火': 'ひ',
        '水': 'みず',
        '土': 'つち',
        '木': 'き',
        '金': 'かね',
        '石': 'いし',
        '草': 'くさ',
        '花': 'はな',
        '葉': 'は',
        '根': 'ね',
        '種': 'たね',
        '実': 'み',
        '果': 'か',
        '森': 'もり',
        '林': 'はやし',
        '山': 'やま',
        '川': 'かわ',
        '海': 'うみ',
        '空': 'そら',
        '風': 'かぜ',
        '雷': 'かみなり',
        '雪': 'ゆき',
        '氷': 'こおり',
        '炎': 'ほのお',
        '光': 'ひかり',
        '影': 'かげ',
        '音': 'おと',
        '声': 'こえ',
        '目': 'め',
        '口': 'くち',
        '手': 'て',
        '足': 'あし',
        '心': 'こころ',
        '力': 'ちから',
        '技': 'わざ',
        '術': 'じゅつ',
        '道': 'みち',
        '学': 'がく',
        '文': 'ぶん',
        '字': 'じ',
        '語': 'ご',
        '言': 'こと',
        '話': 'はなし',
        '聞': 'き',
        '見': 'み',
        '知': 'し',
        '思': 'おも',
        '考': 'かんが',
        '覚': 'おぼ',
        '忘': 'わす',
        '記': 'き',
        '憶': 'おく',
        '想': 'そう',
        '念': 'ねん',
        '意': 'い',
        '志': 'こころざ',
        '願': 'ねが',
        '望': 'のぞ',
        '夢': 'ゆめ',
        '現': 'あらわ',
        '実': 'じつ',
        '真': 'ま',
        '正': 'ただ',
        '確': 'たし',
        '定': 'さだ',
        '決': 'き',
        '断': 'だん',
        '判': 'はん',
        '別': 'べつ',
        '分': 'わ',
        '解': 'かい',
        '明': 'あか',
        '暗': 'くら',
        '新': 'あたら',
        '古': 'ふる',
        '大': 'おお',
        '小': 'ちい',
        '高': 'たか',
        '低': 'ひく',
        '長': 'なが',
        '短': 'みじか',
        '広': 'ひろ',
        '狭': 'せま',
        '深': 'ふか',
        '浅': 'あさ',
        '重': 'おも',
        '軽': 'かる',
        '強': 'つよ',
        '弱': 'よわ',
        '速': 'はや',
        '遅': 'おそ',
        '早': 'はや',
        '晩': 'ばん',
        '朝': 'あさ',
        '昼': 'ひる',
        '夜': 'よる',
        '今': 'いま',
        '昔': 'むかし',
        '未来': 'みらい',
        '過去': 'かこ',
        '現在': 'げんざい',
        '時間': 'じかん',
        '時': 'とき',
        '分': 'ふん',
        '秒': 'びょう',
        '年': 'とし',
        '月': 'つき',
        '日': 'ひ',
        '週': 'しゅう',
        '曜': 'よう',
        '季節': 'きせつ',
        '春': 'はる',
        '夏': 'なつ',
        '秋': 'あき',
        '冬': 'ふゆ',
        '天': 'てん',
        '地': 'ち',
        '人': 'ひと',
        '物': 'もの',
        '事': 'こと',
        '場': 'ば',
        '所': 'ところ',
        '方': 'かた',
        '辺': 'へん',
        '中': 'なか',
        '外': 'そと',
        '内': 'うち',
        '上': 'うえ',
        '下': 'した',
        '前': 'まえ',
        '後': 'うしろ',
        '左': 'ひだり',
        '右': 'みぎ',
        '東': 'ひがし',
        '西': 'にし',
        '南': 'みなみ',
        '北': 'きた',
        '中央': 'ちゅうおう',
        '中心': 'ちゅうしん',
        '周': 'まわ',
        '回': 'まわ',
        '転': 'ころ',
        '動': 'うご',
        '静': 'しず',
        '止': 'と',
        '進': 'すす',
        '退': 'しりぞ',
        '来': 'き',
        '去': 'さ',
        '帰': 'かえ',
        '出': 'で',
        '入': 'はい',
        '開': 'ひら',
        '閉': 'し',
        '始': 'はじ',
        '終': 'お',
        '続': 'つづ',
        '続': 'つづ',
        '変': 'か',
        '化': 'か',
        '成': 'な',
        '立': 'た',
        '建': 'たて',
        '作': 'つく',
        '造': 'つく',
        '生': 'う',
        '産': 'う',
        '育': 'そだ',
        '養': 'やしな',
        '教': 'おし',
        '習': 'なら',
        '練': 'ね',
        '修': 'しゅう',
        '研': 'けん',
        '究': 'きゅう',
        '発': 'はつ',
        '見': 'み',
        '発見': 'はっけん',
        '発明': 'はつめい',
        '創造': 'そうぞう',
        '制作': 'せいさく',
        '生産': 'せいさん',
        '製造': 'せいぞう',
        '開発': 'かいはつ',
        '設計': 'せっけい',
        '計画': 'けいかく',
        '準備': 'じゅんび',
        '実行': 'じっこう',
        '実現': 'じつげん',
        '完成': 'かんせい',
        '成功': 'せいこう',
        '失敗': 'しっぱい',
        '勝利': 'しょうり',
        '敗北': 'はいぼく',
        '戦': 'たたか',
        '闘': 'たたか',
        '競': 'きそ',
        '争': 'あらそ',
        '勝': 'か',
        '負': 'ま',
        '勝負': 'しょうぶ',
        '試合': 'しあい',
        '試練': 'しれん',
        '挑戦': 'ちょうせん',
        '挑': 'いど',
        '戦': 'せん',
        '闘': 'とう',
        '競': 'きょう',
        '争': 'そう',
        '勝': 'しょう',
        '負': 'ふ',
        '試': 'し',
        '練': 'れん',
        '挑': 'ちょう',
        '戦': 'せん',
        '闘': 'とう',
        '競': 'きょう',
        '争': 'そう',
        '勝': 'しょう',
        '負': 'ふ',
        '試': 'し',
        '練': 'れん',
        '挑': 'ちょう'
    };
    
    // Add furigana to kanji characters
    let result = text;
    for (const [kanji, reading] of Object.entries(kanjiReadings)) {
        if (result.includes(kanji)) {
            // Replace kanji with reading for speech synthesis
            result = result.replace(new RegExp(kanji, 'g'), reading);
        }
    }
    
    return result;
}

// Simple speech synthesis function that works better in Firefox
function speakText(text, lang = 'ja-JP') {
    console.log('speakText called with:', text, lang);
    
    // Add furigana readings for kanji if it's Japanese text
    let textToSpeak = text;
    if (lang === 'ja-JP') {
        textToSpeak = addFurigana(text);
        console.log('Original text:', text);
        console.log('Text with furigana:', textToSpeak);
    }
    
    if ('speechSynthesis' in window) {
        console.log('Speech synthesis is available');
        
        // Stop any currently speaking
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        utterance.lang = lang;
        utterance.rate = 0.8;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        console.log('Created utterance with lang:', utterance.lang);
        
        // Get available voices
        const voices = speechSynthesis.getVoices();
        console.log('Available voices:', voices.map(v => `${v.name} (${v.lang})`));
        
        // For Japanese text, prioritize Japanese voices
        if (lang === 'ja-JP') {
            // Try to find a Japanese voice first - be very strict
            const japaneseVoice = voices.find(voice => 
                voice.lang.startsWith('ja') || 
                voice.name.toLowerCase().includes('japanese') ||
                voice.name.toLowerCase().includes('nihongo') ||
                voice.name.toLowerCase().includes('japan')
            );
            
            if (japaneseVoice) {
                console.log('Using Japanese voice:', japaneseVoice.name);
                utterance.voice = japaneseVoice;
            } else {
                console.log('No Japanese voice found, using default voice');
                // Force Japanese language even with default voice
                utterance.lang = 'ja-JP';
            }
        } else {
            // For other languages, try to find appropriate voice
            const japaneseVoice = voices.find(voice => voice.lang.startsWith('ja'));
            if (japaneseVoice) {
                console.log('Using Japanese voice:', japaneseVoice.name);
                utterance.voice = japaneseVoice;
            } else {
                console.log('No Japanese voice found, using default voice');
            }
        }
        
        // Simple error handling with English fallback
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event.error);
            
            // If Japanese failed, try with English
            if (lang === 'ja-JP' && event.error !== 'canceled') {
                console.log('Japanese failed, trying English fallback...');
                const englishUtterance = new SpeechSynthesisUtterance(textToSpeak);
                englishUtterance.lang = 'en-US';
                englishUtterance.rate = 0.8;
                englishUtterance.pitch = 1.0;
                englishUtterance.volume = 1.0;
                
                englishUtterance.onerror = (e) => {
                    console.error('English fallback also failed:', e.error);
                    showTTSNotAvailable();
                };
                
                englishUtterance.onstart = () => {
                    console.log('English fallback started');
                };
                
                englishUtterance.onend = () => {
                    console.log('English fallback finished');
                };
                
                speechSynthesis.speak(englishUtterance);
            } else {
                showTTSNotAvailable();
            }
        };
        
        utterance.onstart = () => {
            console.log('Speech started');
        };
        
        utterance.onend = () => {
            console.log('Speech finished');
        };
        
        console.log('Attempting to speak...');
        speechSynthesis.speak(utterance);
        
    } else {
        console.log('Speech synthesis not supported');
        showTTSNotAvailable();
    }
}

// Show message when TTS is not available
function showTTSNotAvailable() {
    console.log('Speech synthesis not available');
    // Create a temporary notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ff6b6b;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        z-index: 10000;
        font-family: Arial, sans-serif;
        font-size: 14px;
    `;
    notification.textContent = 'Speech synthesis not available. Please try Firefox browser.';
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Function to load JSON files
async function loadData() {
    try {
        const [pokemonResponse, originsResponse, tcgTypesResponse] = await Promise.all([
            fetch('pokemon_base_0001_1025_with_tcg_types.json'),
            fetch('name_origins_0001_1025_cleaned.json'),
            fetch('tcg_types_info.json')
        ]);
        
        pokemonData = await pokemonResponse.json();
        originsData = await originsResponse.json();
        tcgTypesData = await tcgTypesResponse.json();
        
        // Transform data to match the expected format
        const cards = pokemonData.map(pokemon => {
            const origin = originsData[pokemon.ndex] || {};
            const elements = origin.nameOriginElements || [];
            const tcgType = pokemon.tcg_type || 'Colorless';
            const tcgTypeInfo = tcgTypesData[tcgType] || tcgTypesData['Colorless'];
            
            const card = {
                id: pokemon.ndex,
                kana: pokemon.kanaName,
                hiragana: pokemon.hiragana || pokemon.kanaName, // Use hiragana field
                pub: pokemon.publishedName,
                hep: pokemon.hepburnName,
                english: pokemon.english, // Add English name
                img: pokemon.imageUrl,
                jp: elements.slice(1), // Skip the first element (Japanese name)
                en: [], // We'll leave this empty for now
                desc: origin.nameOriginDescription || "",
                tcgType: tcgType,
                tcgTypeIcon: tcgTypeInfo?.icon_url || null
            };
            
            return card;
        });
        
        console.log('Data transformation complete, cards created:', cards.length);
        
        // Build the flashcards
        buildSheets(cards);
        buildPager();
        
        // Add resize listener for mobile responsiveness
        window.addEventListener('resize', () => {
            buildSheets(cards);
            buildPager();
        });
        
        // Add orientation change listener for mobile devices
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                buildSheets(cards);
                buildPager();
            }, 100);
        });
        
        // Add scroll-based navigation for mobile devices
        console.log('Setting up mobile scroll navigation...');
        if (isMobileDevice()) {
            console.log('Mobile device detected, initializing scroll navigation');
            let currentCardIndex = 0;
            let isScrolling = false;
            let lastScrollTop = 0;
            let isNavigating = false; // Flag to prevent scroll events during navigation
            
            // Function to navigate to a specific card
            navigateToCard = function(index) {
                console.log('navigateToCard called with index:', index);
                
                if (index < 0 || index >= cards.length * 2) { // *2 because each card has 2 faces
                    console.log('Invalid index, returning');
                    return;
                }
                
                isNavigating = true; // Set flag to prevent scroll events during navigation
                currentCardIndex = index;
                const sheets = document.querySelectorAll('.sheet');
                console.log('Found sheets:', sheets.length);
                
                // For mobile, scroll to the target sheet instead of hiding/showing
                if (isMobileDevice()) {
                    const targetSheet = sheets[currentCardIndex];
                    if (targetSheet) {
                        targetSheet.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        console.log(`Scrolled to sheet ${currentCardIndex}`);
                    } else {
                        console.log('Target sheet not found!');
                    }
                } else {
                    // Desktop behavior - hide all sheets
                    sheets.forEach((sheet, i) => {
                        sheet.classList.add('hidden');
                    });
                    
                    // Show the current sheet
                    if (sheets[currentCardIndex]) {
                        sheets[currentCardIndex].classList.remove('hidden');
                        console.log(`Sheet ${currentCardIndex} shown`);
                    } else {
                        console.log('Current sheet not found!');
                    }
                }
                
                // Update pager to reflect current page (for mobile, this is more complex)
                const pager = document.getElementById('pager');
                if (pager && !isMobileDevice()) {
                    const pageButtons = pager.querySelectorAll('button');
                    pageButtons.forEach((btn, idx) => {
                        btn.classList.remove('active');
                        if (idx === Math.floor(currentCardIndex / 2) + 2) { // Convert face index to card index
                            btn.classList.add('active');
                        }
                    });
                    console.log('Pager updated');
                }
                
                console.log('Navigation complete');
                
                // Reset navigation flag after a longer delay to allow scroll events to settle
                setTimeout(() => {
                    isNavigating = false;
                    console.log('Navigation flag reset');
                }, 200);
            };
            
            // Make navigateToCard globally accessible for pager integration
            window.navigateToCard = navigateToCard;
            
            // Simple scroll tracking for mobile - no virtual scrolling
            let scrollTimeout;
            window.addEventListener('scroll', (e) => {
                // Throttle scroll events to improve performance
                if (scrollTimeout) {
                    return;
                }
                
                scrollTimeout = setTimeout(() => {
                    scrollTimeout = null;
                    // Simple scroll tracking without hiding cards
                    const sheets = document.querySelectorAll('.sheet');
                    const viewportCenter = window.pageYOffset + window.innerHeight / 2;
                    
                    // Find which card is currently in the center of viewport
                    for (let i = 0; i < sheets.length; i++) {
                        const sheet = sheets[i];
                        const rect = sheet.getBoundingClientRect();
                        const sheetTop = rect.top + window.pageYOffset;
                        const sheetBottom = sheetTop + rect.height;
                        
                        if (viewportCenter >= sheetTop && viewportCenter <= sheetBottom) {
                            currentCardIndex = i;
                            break;
                        }
                    }
                }, 16); // ~60fps throttling
            });
            
            // Initialize to first card
            console.log('Initializing to first card');
            navigateToCard(0);
            console.log('Mobile scroll navigation setup complete');
        }
    } catch (error) {
        console.error('Error loading data:', error);
        document.body.innerHTML = '<h1>Error loading data</h1><p>Please make sure the JSON files are available.</p>';
    }
}

const jpFace = c => `<div class='card' data-tcg-type='${c.tcgType}'><div class='card-header'><div class='type-icon'>${c.tcgTypeIcon ? `<img src='${c.tcgTypeIcon}' alt='${c.tcgType}'/>` : ''}</div></div><div class='card-title'><span class='english-name'>${c.english}</span><span class='japanese-name'>${c.pub} (${c.kana})<button class='speak-btn' onclick='speakText("${c.kana}", "ja-JP")' title='Speak'>🔊</button></span></div><div class='line'></div><div class='image-box'><div class='frame'><img src='${c.img}' alt='${c.kana}'/></div></div><div class='section'>日本語で名前の意味</div><div class='content'>${c.jp.map(t=>`<p>・${t}</p>`).join('')}</div></div>`;

const enFace = c => `<div class='card' data-tcg-type='${c.tcgType}'><div class='card-header'><div class='type-icon'>${c.tcgTypeIcon ? `<img src='${c.tcgTypeIcon}' alt='${c.tcgType}'/>` : ''}</div></div><div class='card-title'><span class='english-name'>${c.english}</span><span class='japanese-name'>${c.pub} (${c.kana})<button class='speak-btn' onclick='speakText("${c.pub}", "ja-JP")' title='Speak'>🔊</button></span></div><div class='line'></div><div class='image-box'><div class='frame'><img src='${c.img}' alt='${c.english}'/></div></div><div class='section'>Name Origin</div><div class='content'>${c.en.map(t=>`<p>・${t}</p>`).join('')}<p style='margin-top:6px'>${c.desc}</p><p style='margin-top:6px'><strong>English:</strong> ${c.english}</p></div></div>`;

function buildSheets(cards) {
    const container = document.getElementById('sheets');
    let html = '';
    
    // Check if we're on mobile - use more reliable detection
    const isMobile = isMobileDevice();
    console.log('buildSheets called, isMobile:', isMobile, 'cards.length:', cards.length);
    
    if (isMobile) {
        // On mobile, create a single long scrollable container with all card faces
        html += "<div class='mobile-scroll-container'>";
        for (let i = 0; i < cards.length; i++) {
            const card = cards[i];
            // Create separate sections for Japanese and English faces
            html += "<section class='sheet card-face'>";
            html += jpFace(card);
            html += "</section>";
            html += "<section class='sheet card-face'>";
            html += enFace(card);
            html += "</section>";
        }
        html += "</div>";
        
        console.log('Mobile layout generated, sections:', cards.length * 2);
        
        // No virtual scrolling initialization needed for simple scroll layout
    } else {
        // On desktop, use CSS Grid for responsive layout
        for (let i = 0; i < cards.length; i += 4) {
            const group = cards.slice(i, i + 4);
            html += "<section class='sheet'>";
            group.forEach((c, idx) => {
                html += jpFace(c) + enFace(c);
            });
            html += "</section>";
        }
        
        console.log('Desktop layout generated, pages:', Math.ceil(cards.length / 4));
    }
    
    container.innerHTML = html;
    console.log('HTML set to container, container children:', container.children.length);
    
    // Simple verification that layout is working
    setTimeout(() => {
        const sheets = document.querySelectorAll('.sheet');
        const cards = document.querySelectorAll('.card');
        console.log('Layout verification - Sheets:', sheets.length, 'Cards:', cards.length);
        
        if (isMobile && sheets.length > 0) {
            console.log('Mobile layout: All sheets should be visible and scrollable');
        }
    }, 100);
}

function buildPager() {
    const pager = document.getElementById('pager');
    const sheets = [...document.querySelectorAll('.sheet')];
    const totalPages = sheets.length;
    let current = 0;
    
    function generatePaginationHTML(currentPage, totalPages) {
        const delta = 2; // Number of pages to show before and after current
        const range = [];
        const rangeWithDots = [];
        
        for (let i = Math.max(2, currentPage - delta); i <= Math.min(totalPages - 1, currentPage + delta); i++) {
            range.push(i);
        }
        
        if (currentPage - delta > 2) {
            rangeWithDots.push(1, '...');
        } else {
            rangeWithDots.push(1);
        }
        
        rangeWithDots.push(...range);
        
        if (currentPage + delta < totalPages - 1) {
            rangeWithDots.push('...', totalPages);
        } else {
            rangeWithDots.push(totalPages);
        }
        
        let html = `<button id='first'>&laquo;</button><button id='prev'>&lsaquo;</button>`;
        
        rangeWithDots.forEach(item => {
            if (item === '...') {
                html += `<span style="padding: 4px 8px;">...</span>`;
            } else {
                const isActive = item === currentPage + 1;
                html += `<button class='page' data-page='${item-1}'${isActive ? ' class="page active"' : ''}>${item}</button>`;
            }
        });
        
        html += `<button id='next'>&rsaquo;</button><button id='last'>&raquo;</button>`;
        return html;
    }
    
    const render = () => {
        sheets.forEach((s, i) => s.classList.toggle('hidden', i !== current));
        pager.innerHTML = generatePaginationHTML(current, totalPages);
        
        // Re-attach event listeners
        pager.querySelector('#first').disabled = current === 0;
        pager.querySelector('#prev').disabled = current === 0;
        pager.querySelector('#next').disabled = current === totalPages - 1;
        pager.querySelector('#last').disabled = current === totalPages - 1;
        
        // Add click handlers
        pager.addEventListener('click', handlePagerClick);
    };
    
    function handlePagerClick(e) {
        if (e.target.tagName !== 'BUTTON') return;
        
        if (e.target.classList.contains('page')) {
            current = parseInt(e.target.dataset.page);
        } else {
            if (e.target.id === 'first') current = 0;
            else if (e.target.id === 'prev') current = Math.max(0, current - 1);
            else if (e.target.id === 'next') current = Math.min(totalPages - 1, current + 1);
            else if (e.target.id === 'last') current = totalPages - 1;
        }
        
        // For mobile, also update the scroll navigation
        if (isMobileDevice()) {
            // Convert page index to face index (each page has 2 faces)
            const faceIndex = current * 2;
            // Find the global navigateToCard function and call it
            if (window.navigateToCard) {
                window.navigateToCard(faceIndex);
            }
        }
        
        render();
    };
    
    render();
}

// Initialize speech synthesis
function initSpeechSynthesis() {
    console.log('Initializing speech synthesis...');
    
    if ('speechSynthesis' in window) {
        console.log('Speech synthesis API is available');
        
        // Force voices to load
        const initialVoices = speechSynthesis.getVoices();
        console.log('Initial voices count:', initialVoices.length);
        
        // Log available voices for debugging
        speechSynthesis.onvoiceschanged = () => {
            const voices = speechSynthesis.getVoices();
            console.log('=== VOICES LOADED ===');
            console.log('Total voices available:', voices.length);
            console.log('All voices:', voices.map(v => `${v.name} (${v.lang})`));
            
            const japaneseVoices = voices.filter(v => 
                v.lang.startsWith('ja') || 
                v.name.toLowerCase().includes('japanese') ||
                v.name.toLowerCase().includes('nihongo') ||
                v.name.toLowerCase().includes('japan')
            );
            console.log('Japanese voices:', japaneseVoices.map(v => `${v.name} (${v.lang})`));
            
            if (japaneseVoices.length === 0) {
                console.warn('No Japanese voices found! You may need to install Japanese language packs.');
                console.log('Available languages:', [...new Set(voices.map(v => v.lang))]);
                console.log('To install Japanese voices on Linux:');
                console.log('  Ubuntu/Debian: sudo apt-get install speech-dispatcher speech-dispatcher-flite');
                console.log('  Or try: sudo apt-get install espeak-ng-data');
                console.log('  Then restart your browser');
            } else {
                console.log('Japanese voices found! Speech synthesis should work properly.');
            }
        };
        
        // Try to trigger voice loading
        setTimeout(() => {
            console.log('Triggering voice loading...');
            speechSynthesis.getVoices();
        }, 100);
        
    } else {
        console.error('Speech synthesis API not available');
    }
}

// Test function for debugging speech synthesis
window.testSpeech = function() {
    console.log('=== TESTING SPEECH SYNTHESIS ===');
    console.log('Speech synthesis available:', 'speechSynthesis' in window);
    console.log('Current voices:', speechSynthesis.getVoices().map(v => `${v.name} (${v.lang})`));
    speakText('こんにちは', 'ja-JP');
};

// Test with English to see if any speech works
window.testEnglishSpeech = function() {
    console.log('=== TESTING ENGLISH SPEECH ===');
    speakText('Hello world', 'en-US');
};

// Test Japanese pronunciation specifically
window.testJapaneseSpeech = function() {
    console.log('=== TESTING JAPANESE SPEECH ===');
    console.log('Testing various Japanese text types...');
    
    const testTexts = [
        { text: 'こんにちは', desc: 'Hiragana' },
        { text: 'カタカナ', desc: 'Katakana' },
        { text: '漢字', desc: 'Kanji' },
        { text: 'フシギダネ', desc: 'Pokemon name' },
        { text: '不思議', desc: 'Kanji compound' }
    ];
    
    testTexts.forEach((test, index) => {
        setTimeout(() => {
            console.log(`Testing ${test.desc}: ${test.text}`);
            speakText(test.text, 'ja-JP');
        }, index * 3000);
    });
};

// Force reload voices
window.reloadVoices = function() {
    console.log('=== FORCING VOICE RELOAD ===');
    speechSynthesis.getVoices();
    setTimeout(() => {
        const voices = speechSynthesis.getVoices();
        console.log('Voices after reload:', voices.map(v => `${v.name} (${v.lang})`));
    }, 1000);
};

// Debug function to show all available voices
window.showAllVoices = function() {
    console.log('=== ALL AVAILABLE VOICES ===');
    const voices = speechSynthesis.getVoices();
    
    // Group voices by language
    const voicesByLang = {};
    voices.forEach(voice => {
        const lang = voice.lang || 'unknown';
        if (!voicesByLang[lang]) {
            voicesByLang[lang] = [];
        }
        voicesByLang[lang].push(voice.name);
    });
    
    // Show languages with Japanese-related voices first
    const japaneseRelated = Object.keys(voicesByLang).filter(lang => 
        lang.startsWith('ja') || 
        voicesByLang[lang].some(name => 
            name.toLowerCase().includes('japanese') ||
            name.toLowerCase().includes('nihongo') ||
            name.toLowerCase().includes('japan')
        )
    );
    
    console.log('=== JAPANESE-RELATED VOICES ===');
    japaneseRelated.forEach(lang => {
        console.log(`${lang}:`, voicesByLang[lang]);
    });
    
    console.log('=== ALL LANGUAGES ===');
    Object.keys(voicesByLang).sort().forEach(lang => {
        console.log(`${lang}:`, voicesByLang[lang].slice(0, 3)); // Show first 3 voices per language
    });
    
    console.log(`Total voices: ${voices.length}`);
};

document.addEventListener('DOMContentLoaded', () => {
    initSpeechSynthesis();
    loadData();
}); 