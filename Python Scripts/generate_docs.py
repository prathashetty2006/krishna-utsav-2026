import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_documentation():
    doc = Document()

    # Page Setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.header_distance = Inches(0.5)
        section.footer_distance = Inches(0.5)

    # Color Palette Constants
    COLOR_PRIMARY = RGBColor(26, 35, 126)     # Deep Indigo / Navy (#1A237E)
    COLOR_SECONDARY = RGBColor(198, 161, 91)  # Devotional Gold (#C6A15B)
    COLOR_TEXT = RGBColor(33, 33, 33)         # Charcoal Dark (#212121)
    COLOR_MUTED = RGBColor(100, 100, 100)     # Soft Grey (#646464)
    HEX_HEADER_BG = "1A237E"
    HEX_ALT_BG = "F4F6FB"
    HEX_CALLOUT_BG = "FAF8F5"
    HEX_BORDER = "C6A15B"

    # Set default style font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = COLOR_TEXT
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Helper Functions
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_table_borders(table, color="D3D3D3"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_title(text, subtitle_text):
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(36)
        
        p_inst = doc.add_paragraph()
        p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_inst = p_inst.add_run("DR. B.B. HEGDE FIRST GRADE COLLEGE, KUNDAPURA\nDEPARTMENT OF COMPUTER SCIENCE & CULTURAL COMMITTEE")
        run_inst.font.name = 'Arial'
        run_inst.font.size = Pt(12)
        run_inst.font.bold = True
        run_inst.font.color.rgb = COLOR_SECONDARY
        p_inst.paragraph_format.space_after = Pt(36)

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(26)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        p.paragraph_format.space_after = Pt(12)

        p_sub = doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_sub = p_sub.add_run(subtitle_text)
        run_sub.font.name = 'Calibri'
        run_sub.font.size = Pt(14)
        run_sub.font.italic = True
        run_sub.font.color.rgb = COLOR_MUTED
        p_sub.paragraph_format.space_after = Pt(60)

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_callout(text, title="NOTE"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, HEX_CALLOUT_BG)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_BORDER}"/>'
            f'<w:top w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.1)
        p.paragraph_format.right_indent = Inches(0.1)
        
        r_title = p.add_run(f"[{title}] ")
        r_title.bold = True
        r_title.font.color.rgb = COLOR_SECONDARY
        
        r_text = p.add_run(text)
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = COLOR_TEXT
        
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_code_block(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "2B2D42") # Dark terminal bg
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.1)
        
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(240, 240, 240)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==========================================
    # COVER PAGE
    # ==========================================
    add_title(
        "KRISHNA UTSAV 2K26\nDIGITAL EVENT MANAGEMENT PORTAL",
        "A High-Performance Containerized Web Platform for Cultural Festival Coordination"
    )

    # Submission Table Box
    sub_table = doc.add_table(rows=5, cols=2)
    sub_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sub_table, "E0E0E0")
    
    meta_data = [
        ("Course / Degree:", "Bachelor of Computer Applications (B.C.A) / B.Sc CS"),
        ("Subject / Lab:", "Web Application Development & DevOps Project"),
        ("Institution:", "Dr. B.B. Hegde First Grade College, Kundapura"),
        ("Academic Year:", "2025 - 2026"),
        ("Submission Date:", "August 2026")
    ]
    
    for i, (label, val) in enumerate(meta_data):
        row = sub_table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = Inches(2.2)
        c2.width = Inches(4.3)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(label)
        r1.bold = True
        r1.font.color.rgb = COLOR_PRIMARY
        
        p2 = c2.paragraphs[0]
        r2 = p2.add_run(val)
        r2.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # Setup Header & Footer for main body
    body_section = doc.sections[0]
    header = body_section.header
    p_head = header.paragraphs[0]
    p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_head = p_head.add_run("Krishna Utsav 2K26 | Project Documentation & Architecture")
    r_head.font.size = Pt(8.5)
    r_head.font.color.rgb = COLOR_MUTED

    footer = body_section.footer
    p_foot = footer.paragraphs[0]
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run("Dr. B.B. Hegde First Grade College - Department of Computer Science")
    r_foot.font.size = Pt(9)
    r_foot.font.color.rgb = COLOR_MUTED

    # ==========================================
    # EXECUTIVE SUMMARY / ABSTRACT
    # ==========================================
    add_heading_1("Executive Summary & Abstract")
    p_abs = doc.add_paragraph(
        "The Krishna Utsav 2K26 Web Portal is an industry-grade, responsive digital event management "
        "and cultural showcase platform built specifically for Dr. B.B. Hegde First Grade College, Kundapura. "
        "The application serves as a centralized hub for managing annual Sri Krishna Janmashtami celebrations, "
        "enabling students, faculty, and visitors to explore cultural competitions, view real-time festival timelines, "
        "browse photo galleries, and access ambient devotional experiences."
    )
    p_abs2 = doc.add_paragraph(
        "Architecturally, the project follows modern enterprise static delivery principles using lightweight Nginx Alpine "
        "containerization orchestrated via Docker and Docker Compose. The user interface leverages vanilla HTML5, custom "
        "CSS3 design systems with glassmorphism aesthetics, and ES6+ JavaScript modules incorporating gesture-aware audio APIs, "
        "dynamic reading progress tracking, responsive navigation drawers, and physics-driven background animations."
    )
    
    add_callout(
        "This project documentation adheres to standardized academic and industry software documentation standards, "
        "covering system requirement analysis, structural project layouts, component logic breakdown, Docker deployment, quality assurance, "
        "and automated documentation synchronization procedures.",
        title="ACADEMIC NOTE"
    )

    # ==========================================
    # TABLE OF CONTENTS OUTLINE
    # ==========================================
    add_heading_1("Table of Contents")
    toc_table = doc.add_table(rows=10, cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(toc_table, "D3D3D3")
    
    toc_data = [
        ("1. Introduction & Project Scope", "Page 3"),
        ("2. Technology Stack & Technical Specifications", "Page 4"),
        ("3. System Architecture & Directory Layout", "Page 5"),
        ("4. System Modules & Functional Features", "Page 6"),
        ("5. Technical Code Breakdown & Implementation", "Page 8"),
        ("6. Containerization & Server Deployment", "Page 11"),
        ("7. Verification, Testing & Quality Assurance", "Page 12"),
        ("8. Documentation Synchronization & Automated Maintenance Rule", "Page 13"),
        ("9. Future Roadmap & Conclusion", "Page 14"),
        ("10. Appendices & References", "Page 15")
    ]
    
    for i, (sec_name, pg_num) in enumerate(toc_data):
        row = toc_table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = Inches(5.2)
        c2.width = Inches(1.3)
        if i % 2 == 1:
            set_cell_background(c1, HEX_ALT_BG)
            set_cell_background(c2, HEX_ALT_BG)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(sec_name)
        r1.font.bold = True
        
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r2 = p2.add_run(pg_num)
        r2.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # ==========================================
    # SECTION 1: INTRODUCTION & PROJECT SCOPE
    # ==========================================
    add_heading_1("1. Introduction & Project Scope")
    
    add_heading_2("1.1 Background & Problem Statement")
    doc.add_paragraph(
        "Educational institutions frequently organize large-scale cultural events like Janmashtami involving hundreds of "
        "participants across multiple categories (music, dance, art, quizzes, traditional costumes). Traditional manual event coordination "
        "suffers from decentralized communication, physical poster reliance, delayed schedule updates, and poor engagement."
    )
    doc.add_paragraph(
        "To solve these challenges, Krishna Utsav 2K26 was engineered as a single-page interactive portal providing instant access to "
        "competition guidelines, event schedules, location details, interactive modals, and multimedia visual experiences."
    )

    add_heading_2("1.2 Objectives")
    bullet_objs = [
        "Provide a visually captivating, modern web interface reflecting traditional spiritual aesthetics with custom corner ornaments and mandala rotations.",
        "Implement a responsive multi-card carousel system for effortless event discovery across mobile, tablet, and desktop devices.",
        "Deliver ambient devotional audio with browser user-gesture policy compliance.",
        "Include interactive UX utilities such as a reading progress scrollbar, scroll-to-top button, and modal portal access.",
        "Containerize the application stack using Docker and Nginx for 100% environment reproducibility and instant cloud deployment.",
        "Maintain automated synchronization between project codebase updates and official Word documentation (.docx)."
    ]
    for b in bullet_objs:
        p = doc.add_paragraph(b, style='List Bullet')
        p.paragraph_format.space_after = Pt(3)

    add_heading_2("1.3 Target Audience & Stakeholders")
    doc.add_paragraph(
        "The primary stakeholders include college students participating in competitions, faculty coordinators managing events, "
        "college administrators reviewing registrations, and external guests visiting the campus during celebrations."
    )

    # ==========================================
    # SECTION 2: TECHNOLOGY STACK
    # ==========================================
    add_heading_1("2. Technology Stack & Technical Specifications")
    
    add_heading_2("2.1 Front-End Core Technologies")
    tech_table = doc.add_table(rows=7, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tech_table, "CCCCCC")
    
    hdr_cells = tech_table.rows[0].cells
    hdr_titles = ["Layer", "Technology / Library", "Role & Purpose"]
    widths = [Inches(1.5), Inches(2.2), Inches(2.8)]
    for idx, name in enumerate(hdr_titles):
        hdr_cells[idx].width = widths[idx]
        set_cell_background(hdr_cells[idx], HEX_HEADER_BG)
        p = hdr_cells[idx].paragraphs[0]
        r = p.add_run(name)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    stack_data = [
        ("Markup", "HTML5 (Semantic)", "DOM structure, ARIA accessibility tags, metadata & sectioning"),
        ("Styling", "CSS3 Custom Variables", "Glassmorphism UI, gradient overlays, keyframe animations & flex/grid layout"),
        ("Scripting", "Vanilla JavaScript (ES6+)", "Carousel sliders, DOM events, audio controls, reading bar & screen-saver math"),
        ("Typography", "Google Fonts (Cinzel / Poppins)", "Cinzel for spiritual heading titles & Poppins for clean body text"),
        ("Icons", "FontAwesome 6.7.2", "Vector icons for location, time, buttons, audio player & timeline markers"),
        ("Server Engine", "Nginx Alpine 1.25+", "Lightweight static web server with Gzip compression & custom routing")
    ]
    
    for row_idx, data in enumerate(stack_data, start=1):
        row = tech_table.rows[row_idx]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.width = widths[col_idx]
            if row_idx % 2 == 0:
                set_cell_background(cell, HEX_ALT_BG)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            if col_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_heading_2("2.2 System & Deployment Requirements")
    doc.add_paragraph(
        "The project is engineered for zero-dependency execution on host machines using Docker containerization. "
        "Minimum hardware and software requirements:"
    )
    req_bullets = [
        "Operating System: Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+ LTS).",
        "Container Runtime: Docker Engine 20.10+ & Docker Compose v2.0+.",
        "RAM: 512 MB minimum (1 GB recommended for Docker engine overhead).",
        "Disk Space: ~25 MB for Nginx Alpine image and project static files."
    ]
    for b in req_bullets:
        doc.add_paragraph(b, style='List Bullet')

    doc.add_page_break()

    # ==========================================
    # SECTION 3: SYSTEM ARCHITECTURE
    # ==========================================
    add_heading_1("3. System Architecture & Directory Layout")
    
    add_heading_2("3.1 High-Level Containerized Architecture")
    doc.add_paragraph(
        "The application utilizes a single-container micro-service pattern where static client assets are bundled directly "
        "into a hardened Nginx Alpine image. Port 8080 on the host system is bound to port 80 inside the container."
    )
    
    arch_code = (
        "+-----------------------------------------------------------------------+\n"
        "|                             CLIENT BROWSER                            |\n"
        "|  (Sends HTTP GET request to http://localhost:8080/HTML%20and%20CSS/index.html) |\n"
        "+----------------------------------+------------------------------------+\n"
        "                                   | (Port 8080 Mapping)\n"
        "                                   v\n"
        "+----------------------------------+------------------------------------+\n"
        "|                         DOCKER CONTAINER                              |\n"
        "|                   (Container Name: janmashtami_portal)                 |\n"
        "|                                                                       |\n"
        "|   +---------------------------------------------------------------+   |\n"
        "|   |                     NGINX ALPINE WEB SERVER                   |   |\n"
        "|   |  - Listens on Port 80                                         |   |\n"
        "|   |  - Gzip Compression Enabled (CSS, JS, Fonts, Audio)           |   |\n"
        "|   |  - Root Directory: /usr/share/nginx/html                      |   |\n"
        "|   +-------------------------------+-------------------------------+   |\n"
        "|                                   |                                   |\n"
        "|   +-------------------------------+-------------------------------+   |\n"
        "|   |                     PROJECT STATIC ASSETS                     |   |\n"
        "|   |  - HTML and CSS/ (index.html, index.css)                        |\n"
        "|   |  - Java Script/ (index.js)                                    |\n"
        "|   |  - Image and Audio/ (peacock-feather, audio, images)          |\n"
        "|   +---------------------------------------------------------------+   |\n"
        "+-----------------------------------------------------------------------+"
    )
    add_code_block(arch_code)

    add_heading_2("3.2 Project Workspace Directory Layout")
    doc.add_paragraph(
        "The repository is structured according to strict separation-of-concerns guidelines to ensure high maintainability:"
    )

    dir_table = doc.add_table(rows=9, cols=3)
    dir_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(dir_table, "CCCCCC")
    
    d_hdr = dir_table.rows[0].cells
    d_hdr[0].width = Inches(1.8)
    d_hdr[1].width = Inches(2.2)
    d_hdr[2].width = Inches(2.5)
    for idx, hname in enumerate(["Directory / File", "Contents", "Purpose"]):
        set_cell_background(d_hdr[idx], HEX_HEADER_BG)
        p = d_hdr[idx].paragraphs[0]
        r = p.add_run(hname)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    dir_data = [
        ("index.html, vercel.json", "Root entry files", "Zero-config root entry point for Vercel, Netlify, and Cloud CDNs to prevent 404s"),
        ("HTML and CSS/", "index.html, index.css", "Semantic structure, layout templates, glassmorphism design tokens"),
        ("Java Script/", "index.js", "Client interaction, carousels, audio gesture handlers, screensaver logic"),
        ("Data and Config/", "nginx.conf", "Custom Nginx web server configuration, Gzip types & redirect rules"),
        ("Image and Audio/", "Flute audio, photos", "Devotional background audio (mp3), peacock feather textures & images"),
        ("Python Scripts/", "generate_docs.py, create_root_entry.py", "Automated Word documentation and root HTML synchronization scripts"),
        ("Docs and Notes/", ".docx documentation", "Formal project documentation files created for college submission"),
        ("Root Configs", "Dockerfile, compose, AGENTS.md", "Docker build container, Compose service & Workspace doc sync rules")
    ]

    for r_idx, d_row in enumerate(dir_data, start=1):
        row = dir_table.rows[r_idx]
        for c_idx, val in enumerate(d_row):
            cell = row.cells[c_idx]
            if r_idx % 2 == 0:
                set_cell_background(cell, HEX_ALT_BG)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            if c_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==========================================
    # SECTION 4: MODULES & FEATURES
    # ==========================================
    add_heading_1("4. System Modules & Functional Features")
    
    add_heading_2("4.1 Devotional Hero & Ambient Audio Module")
    doc.add_paragraph(
        "The hero section acts as the primary visual entrance to the portal. It incorporates:"
    )
    h_features = [
        "Spiritual Mandala & Aura Glow: Animated rotating SVG mandala background with multi-layered gold glow rings (outer halo, inner halo, divine aura) surrounding Lord Krishna imagery.",
        "Gesture-Aware Ambient Audio Player: Modern browsers enforce strict autoplay restrictions on audio elements. The system registers a one-time global user gesture listener ('click' or 'touchstart') to initiate background flute playback seamlessly upon first user interaction.",
        "Corner Ornaments & Decorative Flourishes: Four corner ornamental borders (top-left, top-right, bottom-left, bottom-right) reinforcing traditional artistic themes.",
        "Typography & CTA: Uses Cinzel typography for gold accent titles ('2K26') and smooth anchor scroll action buttons ('Explore Events')."
    ]
    for h in h_features:
        doc.add_paragraph(h, style='List Bullet')

    add_heading_2("4.2 Interactive Competition Showcase (6 Featured Festival Events)")
    doc.add_paragraph(
        "The portal highlights 6 official cultural competitions and art events arranged in chronological ascending order by event date and time, "
        "along with designated faculty coordinators, bidding rules, venues, and timings on an interactive, multi-card responsive slider track:"
    )
    
    comp_table = doc.add_table(rows=7, cols=5)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(comp_table, "CCCCCC")
    
    c_hdr = comp_table.rows[0].cells
    widths = [Inches(1.4), Inches(1.1), Inches(1.1), Inches(1.3), Inches(1.6)]
    for idx, hname in enumerate(["Competition Event", "Date & Time", "Event Venue", "Faculty Coordinator", "Description"]):
        c_hdr[idx].width = widths[idx]
        set_cell_background(c_hdr[idx], HEX_HEADER_BG)
        p = c_hdr[idx].paragraphs[0]
        r = p.add_run(hname)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    comp_data = [
        ("Rangoli", "10-09-2026\n9:30 AM", "Auditorium", "Mrs. Nirmala", "Vibrant Rangoli designs incorporating peacock feathers, flutes, and traditional motifs."),
        ("Bhagavadgeethe Shloka Patana", "10-09-2026\n3:00 PM", "AV Hall", "Mrs. Wilma", "Sacred recitation and philosophical chanting from Srimad Bhagavad Gita."),
        ("Kathavachana", "11-09-2026\n3:00 PM", "AV Hall", "Mrs. Vijayashree", "Traditional narrative storytelling and discourse celebrating Sri Krishna Leela."),
        ("Bhajana Sparde", "15-09-2026\n3:00 PM", "AV Hall", "Mr. Giriraj Bhat", "Solo and group devotional singing honoring Lord Krishna's divine qualities."),
        ("Chitra Kala Auction", "16-09-2026\nMorning (10 AM)", "Main Courtyard", "Classroom Bidding\n(₹100 - ₹1,000)", "Grand exhibition of 25+ handmade sketches. Each class purchases at least one artwork via bidding."),
        ("Mosaru Kudike", "16-09-2026\nGrand Finale", "Main Courtyard", "Mr. Pranam &\n Mr. Shreekanth", "Pot decoration contest followed by festive Dahi Handi pot-breaking celebration.")
    ]

    for r_idx, c_row in enumerate(comp_data, start=1):
        row = comp_table.rows[r_idx]
        for c_idx, val in enumerate(c_row):
            cell = row.cells[c_idx]
            cell.width = widths[c_idx]
            if r_idx % 2 == 0:
                set_cell_background(cell, HEX_ALT_BG)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            if c_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_heading_2("4.3 Physics-Based Bouncing Peacock Feathers Screensaver")
    doc.add_paragraph(
        "A signature interactive visual feature of the portal is the dual bouncing peacock feathers background screen saver. "
        "Two high-resolution PNG feather elements continuously move across the viewport, bouncing off window borders with smooth 2D velocity vectors "
        "and subtle angular rotation computed frame-by-frame via requestAnimationFrame()."
    )

    add_heading_2("4.4 User Experience & Navigation Utilities")
    ux_bullets = [
        "Streamlined Static Navigation: Responsive navigation bar featuring direct in-page anchor links (Home, About, Events, Schedule, Gallery, Contact) optimized for zero-overhead static deployment without dynamic profile/session dependencies.",
        "Reading Progress Bar: A dynamic top bar that calculates document scroll depth percentage and fills across the top of the screen in real-time.",
        "Mobile Navigation Drawer: Toggle button converting top navigation into a sleek full-screen drawer on mobile viewports.",
        "Scroll-to-Top Floating Button: Smoothly scrolls the window back to the top when the user scrolls past 400px."
    ]
    for u in ux_bullets:
        doc.add_paragraph(u, style='List Bullet')

    add_heading_2("4.5 Mobile Touch Gesture Support & Unified Triple Carousel System")
    doc.add_paragraph(
        "To provide a seamless, interactive user experience and eliminate awkward multi-row grid wrapping when adding events (e.g. 5 or 6 items), "
        "the portal standardizes a unified Triple Carousel architecture across: (1) Competition Categories, (2) Event Timeline / Schedule, and (3) Celebration Gallery. "
        "Each section features responsive '<' and '>' toggle buttons, boundary-aware disabled states, and fluid touch swipe gesture detection."
    )
    doc.add_paragraph(
        "Users can slide horizontally through all festival timeline milestones without broken grid rows. On mobile screens (under 768px), "
        "the carousel controls automatically reposition to the bottom center for comfortable one-handed thumb navigation."
    )

    add_heading_2("4.6 Fixed Navigation Scroll Offset & Clean Viewport Calibration")
    doc.add_paragraph(
        "A notorious usability defect in single-page web applications with sticky or fixed headers is that clicking anchor navigation links "
        "causes target section titles to be partially or completely obscured behind the navigation bar. The Krishna Utsav portal permanently "
        "resolves this through CSS 'scroll-padding-top: 85px' at root level paired with 'scroll-margin-top: 85px' (75px on mobile) on every section."
    )
    doc.add_paragraph(
        "To guarantee an uncluttered visual hierarchy on small screens, decorative corner ornaments are automatically suppressed on mobile "
        "viewports via media queries, background feather opacity is attenuated to 0.05, and divine hero halo dimensions are scaled adaptively."
    )

    add_heading_2("4.7 Authentic Campus Celebration Gallery Showcase")
    doc.add_paragraph(
        "The celebration gallery features authentic high-resolution photographic documentation captured directly at Dr. B.B. Hegde "
        "First Grade College during the Sri Krishna Janmashtami celebrations. Replacing generic placeholder assets, these four official "
        "photographs capture the spiritual and cultural essence of the institution:"
    )
    gallery_items = [
        "Inaugural Lamp Lighting Ceremony: Traditional lighting of the sacred brass deepa on the AV Hall stage by esteemed college dignitaries, principal, and faculty coordinators in ceremonial attire.",
        "Classical Flute & Devotional Recital: Live stage musical performance featuring students playing classical bamboo flutes and mridangam accompanied by devotional chanting.",
        "Spiritual Discourse (Kathavachana): Keynote address and benediction delivered from the dais commemorating Sri Krishna Leela and timeless ethical teachings.",
        "Presidential Remarks & Felicitation: Formal presidential address and cultural felicitation honoring participants, judges, and organizing committee members."
    ]
    for g in gallery_items:
        doc.add_paragraph(g, style='List Bullet')

    doc.add_paragraph(
        "Each photo card incorporates a multi-layer gradient backing, devotional category tag icon, title typography, "
        "and cubic-bezier hover zoom animation to provide an exhibition-grade viewing experience."
    )

    add_heading_2("4.8 Sacred 11-Alankara Krishna Continuous Darshan Slideshow")
    doc.add_paragraph(
        "In the primary 'About Krishna Janmashtami' section, the single static hero illustration is enhanced with an authentic "
        "11-Alankara sacred darshan slideshow displaying high-resolution photographs of Lord Krishna (located in 'Image and Audio/Krishna/'). "
        "This dynamic component presents the deity in eleven distinct traditional festive alankaras and temple adornments."
    )
    darshan_features = [
        "Continuous 3-Second Auto-Progression: The slider automatically transitions every 3.0 seconds (3,000ms) with smooth 700ms cubic-bezier translation curves.",
        "Infinite Seamless Loop Architecture: Employs a zero-stutter cloned boundary technique (11 real slides + 1 seamless clone) that silently snaps from index 11 back to index 0 on transitionend, delivering an unbroken forward-gliding motion without jarring rewinds.",
        "Real-Time Golden Progress Bar: A 4px glowing gold gradient timer bar fills continuously across the bottom of the active image frame over 3 seconds, giving clear visual cues of countdown progression.",
        "Active Darshan Counter & Header Badge: Displays an ornate gold 'ॐ DIVINE DARSHAN' title header alongside a live-updating counter badge ('1 / 11' through '11 / 11').",
        "11 Pagination Indicator Dots: Interactive navigation dots with a stretched gold pill animation for the currently active slide, allowing one-click jumping to any specific darshan.",
        "Touch Swipe Gesture & Overlay Navigation: Supports touch swipe gestures on mobile viewports as well as glassmorphic Next/Previous chevron buttons.",
        "Intelligent Pause-on-Hover: Automatically freezes slider progression when the user moves their cursor over an idol image, allowing unhurried devotion and detailed viewing."
    ]
    for d in darshan_features:
        doc.add_paragraph(d, style='List Bullet')

    doc.add_page_break()

    # ==========================================
    # SECTION 5: TECHNICAL CODE BREAKDOWN
    # ==========================================
    add_heading_1("5. Technical Code Breakdown & Implementation")
    
    add_heading_2("5.1 Audio Autoplay & Gesture Recognition (Java Script/index.js)")
    doc.add_paragraph(
        "The following snippet demonstrates how browser audio policy compliance is enforced without throwing user-rejection exceptions:"
    )
    js_audio_snippet = (
        "function initAmbientAudio() {\n"
        "    const music = document.getElementById('bgMusic');\n"
        "    if (!music) return;\n\n"
        "    function playAudioOnGesture() {\n"
        "        music.play()\n"
        "            .then(() => console.log('Ambient devotional music started.'))\n"
        "            .catch(e => console.log('Audio playback notice:', e));\n\n"
        "        document.removeEventListener('click', playAudioOnGesture);\n"
        "        document.removeEventListener('touchstart', playAudioOnGesture);\n"
        "    }\n\n"
        "    document.addEventListener('click', playAudioOnGesture);\n"
        "    document.addEventListener('touchstart', playAudioOnGesture);\n"
        "}"
    )
    add_code_block(js_audio_snippet)

    add_heading_2("5.2 Scroll Progress & Reveal Animations (Java Script/index.js)")
    doc.add_paragraph(
        "Scroll reading progress calculation and scroll-to-top button activation:"
    )
    js_scroll_snippet = (
        "function onScroll() {\n"
        "    const scrollTop = window.scrollY || document.documentElement.scrollTop;\n"
        "    const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;\n\n"
        "    if (scrollProgress && docHeight > 0) {\n"
        "        const pct = (scrollTop / docHeight) * 100;\n"
        "        scrollProgress.style.width = `${pct}%`;\n"
        "    }\n"
        "    if (scrollTopBtn) {\n"
        "        if (scrollTop > 400) scrollTopBtn.classList.add('visible');\n"
        "        else scrollTopBtn.classList.remove('visible');\n"
        "    }\n"
        "}"
    )
    add_code_block(js_scroll_snippet)

    add_heading_2("5.3 Custom Nginx Web Server Configuration (Data and Config/nginx.conf)")
    doc.add_paragraph(
        "The custom Nginx config enforces Gzip compression across all mime types and rewrites root requests directly to the HTML entry point:"
    )
    nginx_snippet = (
        "server {\n"
        "    listen 80;\n"
        "    server_name localhost;\n"
        "    absolute_redirect off;\n\n"
        "    location = / {\n"
        "        return 301 /HTML%20and%20CSS/index.html;\n"
        "    }\n\n"
        "    location / {\n"
        "        root /usr/share/nginx/html;\n"
        "        index index.html;\n"
        "    }\n\n"
        "    gzip on;\n"
        "    gzip_types text/plain text/css application/json application/javascript text/xml image/svg+xml audio/mpeg;\n"
        "}"
    )
    add_code_block(nginx_snippet)

    add_heading_2("5.4 Mobile Touch Swipe Gesture Tracking (Java Script/index.js)")
    doc.add_paragraph(
        "To enable smooth swipe navigation on touchscreens, the carousel component tracks touch coordinates and compares start and end offsets:"
    )
    js_touch_snippet = (
        "// Support touch swipe gestures on mobile and touch displays\n"
        "let touchStartX = 0;\n"
        "let touchEndX = 0;\n\n"
        "track.addEventListener('touchstart', (e) => {\n"
        "    touchStartX = e.changedTouches[0].screenX;\n"
        "}, { passive: true });\n\n"
        "track.addEventListener('touchend', (e) => {\n"
        "    touchEndX = e.changedTouches[0].screenX;\n"
        "    const diffX = touchStartX - touchEndX;\n"
        "    if (Math.abs(diffX) > 40) {\n"
        "        if (diffX > 0) {\n"
        "            // Swiped left -> Next item\n"
        "            const maxIndex = cards.length - getVisibleCount();\n"
        "            if (currentIndex < maxIndex) {\n"
        "                currentIndex++;\n"
        "                updateSlider();\n"
        "            }\n"
        "        } else {\n"
        "            // Swiped right -> Previous item\n"
        "            if (currentIndex > 0) {\n"
        "                currentIndex--;\n"
        "                updateSlider();\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "}, { passive: true });"
    )
    add_code_block(js_touch_snippet)

    add_heading_2("5.5 Ergonomic Mobile Carousel & Anchor Offset Rules (HTML and CSS/index.css)")
    doc.add_paragraph(
        "Fixed-header offset rules and bottom-aligned thumb controls on mobile viewports:"
    )
    css_mobile_snippet = (
        "/* Root and section anchor scroll offset compensation */\n"
        "html {\n"
        "    scroll-behavior: smooth;\n"
        "    scroll-padding-top: 85px;\n"
        "}\n\n"
        "section {\n"
        "    scroll-margin-top: 85px;\n"
        "}\n\n"
        "/* Responsive mobile carousel: bottom thumb controls & full-width cards */\n"
        "@media (max-width: 768px) {\n"
        "    .carousel-container {\n"
        "        position: relative;\n"
        "        padding-bottom: 60px;\n"
        "    }\n"
        "    .slider-track .event-card,\n"
        "    .slider-track .timeline-item,\n"
        "    .slider-track .gallery-card {\n"
        "        flex: 0 0 100%;\n"
        "    }\n"
        "    .carousel-ctrl-btn {\n"
        "        position: absolute;\n"
        "        bottom: 0;\n"
        "    }\n"
        "    .carousel-ctrl-btn.prev { left: calc(50% - 55px); }\n"
        "    .carousel-ctrl-btn.next { right: calc(50% - 55px); }\n"
        "}"
    )
    add_code_block(css_mobile_snippet)

    add_heading_2("5.6 Continuous Krishna Darshan Slider Architecture (Java Script/index.js & HTML and CSS/index.css)")
    doc.add_paragraph(
        "The following snippet highlights the requestAnimationFrame-driven 3-second progress timer and seamless loop transition handler:"
    )
    js_slider_snippet = (
        "function initKrishnaDarshanSlider() {\n"
        "    const container = document.getElementById('krishnaSliderContainer');\n"
        "    const track = document.getElementById('krishnaSliderTrack');\n"
        "    const timerBar = document.getElementById('krishnaTimerBar');\n"
        "    const slideDuration = 3000; // 3 seconds per alankara\n"
        "    let currentIndex = 0;\n\n"
        "    // Seamless infinite forward loop via boundary clone\n"
        "    track.addEventListener('transitionend', () => {\n"
        "        isTransitioning = false;\n"
        "        if (currentIndex >= originalCount) {\n"
        "            currentIndex = 0;\n"
        "            renderSlide(false); // snap silently without animation\n"
        "        }\n"
        "    });\n\n"
        "    // 3-second progress timer\n"
        "    function frame(now) {\n"
        "        const elapsed = now - progressStartTime;\n"
        "        const pct = Math.min(100, (elapsed / slideDuration) * 100);\n"
        "        if (timerBar) timerBar.style.width = pct + '%';\n"
        "        if (elapsed < slideDuration) {\n"
        "            animFrameId = requestAnimationFrame(frame);\n"
        "        } else {\n"
        "            nextSlide();\n"
        "            startProgress();\n"
        "        }\n"
        "    }\n"
        "}"
    )
    add_code_block(js_slider_snippet)

    # ==========================================
    # SECTION 6: CONTAINERIZATION & DEPLOYMENT
    # ==========================================
    add_heading_1("6. Containerization & Server Deployment")
    
    add_heading_2("6.1 Dockerfile Specifications")
    doc.add_paragraph(
        "The build uses an official lightweight Nginx Alpine base image (`nginx:alpine`), copies custom configuration rules, and mounts static assets:"
    )
    dockerfile_snippet = (
        "FROM nginx:alpine\n"
        "RUN rm -rf /usr/share/nginx/html/*\n"
        "COPY [\"Data and Config/nginx.conf\", \"/etc/nginx/conf.d/default.conf\"]\n"
        "COPY [\".\", \"/usr/share/nginx/html/\"]\n"
        "EXPOSE 80\n"
        "CMD [\"nginx\", \"-g\", \"daemon off;\"]"
    )
    add_code_block(dockerfile_snippet)

    add_heading_2("6.2 Step-by-Step Build & Run Commands")
    doc.add_paragraph("To build and start the portal using standard Docker CLI:")
    add_code_block("# 1. Build Docker Image\ndocker build -t krishna-utsav-portal .\n\n# 2. Run Container on Port 8080\ndocker run -d -p 8080:80 --name janmashtami_portal krishna-utsav-portal")

    doc.add_paragraph("To launch using Docker Compose:")
    add_code_block("# Start service in detached mode\ndocker-compose up -d\n\n# Stop and remove container\ndocker-compose down")

    add_heading_2("6.3 Cloud Edge Deployment & Vercel Static Hosting Architecture")
    doc.add_paragraph(
        "For global edge delivery without Docker infrastructure, the repository is configured for instantaneous deployment "
        "on Vercel, Netlify, and GitHub Pages. Modern cloud static hosts look for `index.html` at the repository root by default."
    )
    doc.add_paragraph(
        "To prevent 404 routing errors upon initial deployment, the project provides a synchronized root `index.html` with calibrated "
        "relative asset bindings (`HTML and CSS/index.css`, `Java Script/index.js`, `Image and Audio/`), paired with a root `vercel.json` "
        "configuration file enabling clean URLs and resilient path routing."
    )
    add_code_block(
        "// vercel.json - Edge static hosting configuration\n"
        "{\n"
        "  \"cleanUrls\": true,\n"
        "  \"trailingSlash\": false\n"
        "}"
    )

    doc.add_page_break()

    # ==========================================
    # SECTION 7: TESTING & QA
    # ==========================================
    add_heading_1("7. Verification, Testing & Quality Assurance")
    
    add_heading_2("7.1 Responsive Viewport Verification Matrix")
    doc.add_paragraph(
        "The application underwent systematic layout testing across standard resolution breakpoints to ensure seamless visual fidelity:"
    )

    test_table = doc.add_table(rows=6, cols=4)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(test_table, "CCCCCC")
    
    t_hdr = test_table.rows[0].cells
    for idx, hname in enumerate(["Device Type", "Viewport Width", "Layout Behavior", "Status"]):
        set_cell_background(t_hdr[idx], HEX_HEADER_BG)
        p = t_hdr[idx].paragraphs[0]
        r = p.add_run(hname)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_data = [
        ("Mobile Portrait", "< 480px", "Single card carousel, touch swipe gestures, bottom thumb controls, full-width CTA buttons, hidden ornaments", "PASSED [100%]"),
        ("Mobile / Small Tablet", "481px - 768px", "Full-width carousel cards with bottom-centered buttons, 75px fixed-header scroll padding, drawer nav", "PASSED [100%]"),
        ("Tablet Landscape", "769px - 992px", "2-card carousel slider track, side arrows, 85px fixed-header scroll padding", "PASSED [100%]"),
        ("Laptop / Desktop", "1024px - 1440px", "3-card carousel slider track, inline desktop navigation link bar, full halo effects", "PASSED [100%]"),
        ("Ultra-Wide Monitor", "1920px+", "Max-width container clamping (1400px limit), centered hero halo & layout", "PASSED [100%]")
    ]

    for r_idx, t_row in enumerate(test_data, start=1):
        row = test_table.rows[r_idx]
        for c_idx, val in enumerate(t_row):
            cell = row.cells[c_idx]
            if r_idx % 2 == 0:
                set_cell_background(cell, HEX_ALT_BG)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            if c_idx == 3:
                r.bold = True
                r.font.color.rgb = RGBColor(46, 125, 50) # Green success

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==========================================
    # SECTION 8: AUTOMATED DOCUMENTATION MAINTENACE
    # ==========================================
    add_heading_1("8. Documentation Synchronization & Automated Maintenance Rule")
    doc.add_paragraph(
        "To ensure that the project documentation (`Krishna_Utsav_2026_Project_Documentation.docx`) never becomes obsolete when new features, "
        "styling changes, or backend updates are made to the codebase, an explicit workspace rule has been established in `.agents/AGENTS.md`."
    )
    
    add_callout(
        "MANDATORY WORKSPACE RULE: Whenever any new feature, section, style token, script logic, configuration, or file is modified or added to "
        "this repository, the developer or AI assistant MUST update 'Python Scripts/generate_docs.py' and re-run it to regenerate "
        "'Docs and Notes/Krishna_Utsav_2026_Project_Documentation.docx'.",
        title="DOCUMENTATION SYNC REQUIREMENT"
    )

    doc.add_paragraph(
        "This guarantees 100% synchronization between the actual live source code and the official Microsoft Word project documentation submitted for college evaluation."
    )

    # ==========================================
    # SECTION 9: FUTURE ROADMAP & CONCLUSION
    # ==========================================
    add_heading_1("9. Future Roadmap & Conclusion")
    
    add_heading_2("9.1 Recommended Future Extensions")
    future_items = [
        "Backend Database Integration: Introduce a Node.js/Express backend paired with PostgreSQL/MongoDB to process live student registrations.",
        "Automated Email / SMS Notifications: Send instant ticket confirmations and QR code passes upon successful competition registration.",
        "Live Scoreboard & Result Portal: Enable real-time publishing of judge evaluations and winner announcements during festival day.",
        "PWA Support: Add Service Worker caching and Web Manifest to allow offline festival guide viewing on mobile phones."
    ]
    for item in future_items:
        doc.add_paragraph(item, style='List Bullet')

    add_heading_2("9.2 Conclusion")
    doc.add_paragraph(
        "The Krishna Utsav 2K26 Web Portal successfully bridges traditional cultural heritage with modern web development practices. "
        "Through responsive CSS glassmorphism, gesture-compliant Web Audio integration, physics animations, automated documentation synchronization, "
        "and production-ready Docker containerization, the portal offers a robust, scalable, and visually enchanting event management platform suitable for academic presentation and real-world deployment."
    )

    # Save output file in Docs and Notes/
    output_dir = os.path.join(os.getcwd(), "Docs and Notes")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "Krishna_Utsav_2026_Project_Documentation.docx")
    doc.save(output_path)
    print(f"Successfully generated project documentation docx at: {output_path}")

if __name__ == "__main__":
    create_documentation()
