/**
 * ==========================================================================
 * KRISHNA UTSAV 2026 - DIGITAL INVITATION JAVASCRIPT
 * Handles QR Code generation, Download as Image, WhatsApp Sharing, Audio & Copy
 * ==========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    initQrCode();
    initDownloadFeature();
    initWhatsAppShare();
    initCopyFeature();
    initAudioToggle();
});

const PORTAL_URL = 'https://krishna-utsav-2026.vercel.app';

/**
 * Generate high-res QR code for the portal URL
 */
function initQrCode() {
    const qrContainer = document.getElementById('invitationQrCode');
    if (!qrContainer) return;

    // Use QRCode library if loaded, or render high-quality fallback SVG
    if (typeof QRCode !== 'undefined') {
        qrContainer.innerHTML = '';
        new QRCode(qrContainer, {
            text: PORTAL_URL,
            width: 80,
            height: 80,
            colorDark: "#0B132B",
            colorLight: "#FFFFFF",
            correctLevel: QRCode.CorrectLevel.H
        });
    } else {
        // Fallback to QR API image with crisp resolution
        qrContainer.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(PORTAL_URL)}" alt="QR Code to Portal" style="width: 80px; height: 80px; display: block; border-radius: 4px;">`;
    }
}

/**
 * Download Invitation Card as High-Resolution Image using html2canvas
 */
function initDownloadFeature() {
    const downloadBtn = document.getElementById('downloadCardBtn');
    const invitationCard = document.getElementById('invitationCardElement');

    if (!downloadBtn || !invitationCard) return;

    downloadBtn.addEventListener('click', async () => {
        const originalText = downloadBtn.innerHTML;
        downloadBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Generating HD Poster...`;
        downloadBtn.disabled = true;

        try {
            if (typeof html2canvas === 'undefined') {
                await loadScript('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js');
            }

            const canvas = await html2canvas(invitationCard, {
                scale: 2.5, // Crisp 2.5x resolution for print/sharing
                useCORS: true,
                allowTaint: true,
                backgroundColor: '#040814',
                logging: false,
                onclone: (clonedDoc) => {
                    // Optional styling adjustments for canvas capture
                    const clonedCard = clonedDoc.getElementById('invitationCardElement');
                    if (clonedCard) {
                        clonedCard.style.boxShadow = 'none';
                    }
                }
            });

            // Convert to download link
            const imageURL = canvas.toDataURL('image/png');
            const downloadLink = document.createElement('a');
            downloadLink.href = imageURL;
            downloadLink.download = 'Krishna_Janmashtami_2026_Invitation.png';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);

            showToast('🌸 Invitation Poster downloaded successfully!');
        } catch (error) {
            console.error('Error exporting invitation card:', error);
            showToast('⚠️ Could not generate image. Taking screenshot instead.');
            window.print();
        } finally {
            downloadBtn.innerHTML = originalText;
            downloadBtn.disabled = false;
        }
    });
}

/**
 * Share via WhatsApp with festive invite copy
 */
function initWhatsAppShare() {
    const shareBtn = document.getElementById('shareWhatsAppBtn');
    if (!shareBtn) return;

    shareBtn.addEventListener('click', () => {
        const inviteMessage = 
`🌸✨ *Celebrate the Divine Spirit of Krishna Janmashtami 2026* ✨🌸

The *Department of Computer Applications* in association with the *Student Welfare Council*, *Dr. B. B. Hegde First Grade College, Kundapura*, is delighted to invite you to a vibrant and soulful celebration of Shri Krishna Janmashtami! 💫

🎶 Enchanting Cultural Performances
💃 Devotional Music & Traditional Arts
🏆 6 Exciting Competitions & Chitra Kala Auction
🏺 Grand Finale: Mosaru Kudike (Dahi Handi)

🔗 *Register & View Schedule:* ${PORTAL_URL}

We warmly invite you to partake in the celebration and receive divine blessings! 🙏✨`;

        const whatsappUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(inviteMessage)}`;
        window.open(whatsappUrl, '_blank');
    });
}

/**
 * Copy Portal Link to Clipboard
 */
function initCopyFeature() {
    const copyBtn = document.getElementById('copyLinkBtn');
    if (!copyBtn) return;

    copyBtn.addEventListener('click', async () => {
        try {
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(PORTAL_URL);
            } else {
                const tempInput = document.createElement('input');
                tempInput.value = PORTAL_URL;
                document.body.appendChild(tempInput);
                tempInput.select();
                document.execCommand('copy');
                document.body.removeChild(tempInput);
            }
            showToast('🔗 Portal link copied to clipboard!');
        } catch (err) {
            console.error('Copy failed', err);
            showToast('🔗 Link: ' + PORTAL_URL);
        }
    });
}

/**
 * Ambient Audio Toggle
 */
function initAudioToggle() {
    const soundBtn = document.getElementById('invSoundBtn');
    const audio = document.getElementById('invFluteAudio');
    if (!soundBtn || !audio) return;

    soundBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play().then(() => {
                soundBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
                soundBtn.style.color = '#38bdf8';
                showToast('🎶 Divine Flute playing');
            }).catch(e => {
                console.log('Audio autoplay prevented:', e);
            });
        } else {
            audio.pause();
            soundBtn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
            soundBtn.style.color = 'var(--gold-primary)';
            showToast('🔇 Audio paused');
        }
    });
}

/**
 * Display toast notification
 */
function showToast(message) {
    let toast = document.getElementById('invitationToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'invitationToast';
        toast.className = 'invitation-toast';
        document.body.appendChild(toast);
    }
    toast.innerHTML = message;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3200);
}

/**
 * Dynamic script loader helper
 */
function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}
