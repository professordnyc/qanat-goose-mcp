"""
UI Styles and Theme Configuration
Styling constants and theme utilities for Qanat UI components
"""

from typing import Dict, Any

# Color palette
COLORS = {
    # Status colors
    "success": "#28a745",
    "warning": "#ffc107", 
    "error": "#dc3545",
    "info": "#17a2b8",
    "primary": "#007bff",
    "secondary": "#6c757d",
    
    # Background colors
    "success_bg": "#d4edda",
    "warning_bg": "#fff3cd",
    "error_bg": "#f8d7da", 
    "info_bg": "#d1ecf1",
    "primary_bg": "#cce5ff",
    "secondary_bg": "#f8f9fa",
    
    # Text colors
    "success_text": "#155724",
    "warning_text": "#856404",
    "error_text": "#721c24",
    "info_text": "#0c5460",
    "primary_text": "#004085",
    "secondary_text": "#383d41",
    
    # Neutral colors
    "white": "#ffffff",
    "light": "#f8f9fa",
    "gray": "#6c757d",
    "dark": "#343a40",
    "black": "#000000"
}

# Status badge styles
STATUS_BADGE_STYLES = {
    "active": {
        "background": COLORS["success_bg"],
        "color": COLORS["success_text"],
        "border": f"1px solid {COLORS['success']}"
    },
    "inactive": {
        "background": COLORS["error_bg"],
        "color": COLORS["error_text"], 
        "border": f"1px solid {COLORS['error']}"
    },
    "pending": {
        "background": COLORS["warning_bg"],
        "color": COLORS["warning_text"],
        "border": f"1px solid {COLORS['warning']}"
    },
    "completed": {
        "background": COLORS["success_bg"],
        "color": COLORS["success_text"],
        "border": f"1px solid {COLORS['success']}"
    },
    "refunded": {
        "background": COLORS["error_bg"],
        "color": COLORS["error_text"],
        "border": f"1px solid {COLORS['error']}"
    },
    "in_stock": {
        "background": COLORS["success_bg"],
        "color": COLORS["success_text"],
        "border": f"1px solid {COLORS['success']}"
    },
    "low_stock": {
        "background": COLORS["warning_bg"],
        "color": COLORS["warning_text"],
        "border": f"1px solid {COLORS['warning']}"
    },
    "out_of_stock": {
        "background": COLORS["error_bg"],
        "color": COLORS["error_text"],
        "border": f"1px solid {COLORS['error']}"
    }
}

# Button styles
BUTTON_STYLES = {
    "primary": {
        "background": COLORS["primary"],
        "color": COLORS["white"],
        "border": f"1px solid {COLORS['primary']}",
        "hover": {
            "background": "#0056b3",
            "border": "1px solid #0056b3"
        }
    },
    "secondary": {
        "background": COLORS["secondary"],
        "color": COLORS["white"], 
        "border": f"1px solid {COLORS['secondary']}",
        "hover": {
            "background": "#545b62",
            "border": "1px solid #545b62"
        }
    },
    "success": {
        "background": COLORS["success"],
        "color": COLORS["white"],
        "border": f"1px solid {COLORS['success']}",
        "hover": {
            "background": "#1e7e34",
            "border": "1px solid #1e7e34"
        }
    },
    "warning": {
        "background": COLORS["warning"],
        "color": COLORS["dark"],
        "border": f"1px solid {COLORS['warning']}",
        "hover": {
            "background": "#e0a800",
            "border": "1px solid #e0a800"
        }
    },
    "danger": {
        "background": COLORS["error"],
        "color": COLORS["white"],
        "border": f"1px solid {COLORS['error']}",
        "hover": {
            "background": "#c82333",
            "border": "1px solid #c82333"
        }
    },
    "outline": {
        "background": "transparent",
        "color": COLORS["primary"],
        "border": f"1px solid {COLORS['primary']}",
        "hover": {
            "background": COLORS["primary"],
            "color": COLORS["white"]
        }
    }
}

# Table styles
TABLE_STYLES = {
    "header": {
        "background": COLORS["light"],
        "color": COLORS["dark"],
        "font_weight": "600",
        "border_bottom": f"2px solid {COLORS['gray']}"
    },
    "row": {
        "background": COLORS["white"],
        "color": COLORS["dark"],
        "border_bottom": f"1px solid {COLORS['light']}",
        "hover": {
            "background": COLORS["light"]
        }
    },
    "row_selected": {
        "background": COLORS["primary_bg"],
        "color": COLORS["primary_text"]
    }
}

# Loading spinner styles
LOADING_STYLES = {
    "spinner": {
        "color": COLORS["primary"],
        "size": "24px",
        "border_width": "3px"
    },
    "overlay": {
        "background": "rgba(255, 255, 255, 0.8)",
        "backdrop_filter": "blur(2px)"
    }
}

def get_status_badge_style(status: str) -> Dict[str, Any]:
    """Get badge style for a status"""
    status_key = status.lower().replace(" ", "_")
    return STATUS_BADGE_STYLES.get(status_key, STATUS_BADGE_STYLES["inactive"])

def get_button_style(style: str = "primary") -> Dict[str, Any]:
    """Get button style"""
    return BUTTON_STYLES.get(style, BUTTON_STYLES["primary"])

def create_styled_badge(text: str, status: str) -> Dict[str, Any]:
    """Create a styled status badge"""
    style = get_status_badge_style(status)
    
    return {
        "type": "badge",
        "text": text,
        "style": {
            "background_color": style["background"],
            "color": style["color"],
            "border": style["border"],
            "border_radius": "12px",
            "padding": "4px 8px",
            "font_size": "12px",
            "font_weight": "500",
            "display": "inline-block"
        }
    }

def create_styled_button(label: str, action: str, style: str = "primary", params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a styled button"""
    button_style = get_button_style(style)
    
    return {
        "type": "button",
        "label": label,
        "action": action,
        "params": params or {},
        "style": {
            "background_color": button_style["background"],
            "color": button_style["color"],
            "border": button_style["border"],
            "border_radius": "4px",
            "padding": "6px 12px",
            "font_size": "14px",
            "font_weight": "500",
            "cursor": "pointer",
            "transition": "all 0.2s ease"
        },
        "hover_style": button_style.get("hover", {})
    }

def create_loading_overlay(message: str = "Loading...") -> Dict[str, Any]:
    """Create a loading overlay"""
    return {
        "type": "loading_overlay",
        "message": message,
        "style": {
            "position": "absolute",
            "top": "0",
            "left": "0", 
            "right": "0",
            "bottom": "0",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center",
            "background": LOADING_STYLES["overlay"]["background"],
            "backdrop_filter": LOADING_STYLES["overlay"]["backdrop_filter"],
            "z_index": "1000"
        },
        "spinner": {
            "size": LOADING_STYLES["spinner"]["size"],
            "color": LOADING_STYLES["spinner"]["color"],
            "border_width": LOADING_STYLES["spinner"]["border_width"]
        }
    }

def create_notification(message: str, type: str = "info", duration: int = 5000) -> Dict[str, Any]:
    """Create a styled notification"""
    type_styles = {
        "success": {"bg": COLORS["success_bg"], "text": COLORS["success_text"], "border": COLORS["success"]},
        "warning": {"bg": COLORS["warning_bg"], "text": COLORS["warning_text"], "border": COLORS["warning"]},
        "error": {"bg": COLORS["error_bg"], "text": COLORS["error_text"], "border": COLORS["error"]},
        "info": {"bg": COLORS["info_bg"], "text": COLORS["info_text"], "border": COLORS["info"]}
    }
    
    style_config = type_styles.get(type, type_styles["info"])
    
    return {
        "type": "notification",
        "message": message,
        "notification_type": type,
        "duration": duration,
        "style": {
            "background": style_config["bg"],
            "color": style_config["text"],
            "border": f"1px solid {style_config['border']}",
            "border_radius": "4px",
            "padding": "12px 16px",
            "margin": "8px 0",
            "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
        }
    }

def apply_table_styles(table_component: Dict[str, Any]) -> Dict[str, Any]:
    """Apply consistent table styling"""
    table_component["style"] = {
        "border_collapse": "collapse",
        "width": "100%",
        "font_size": "14px",
        "background": COLORS["white"]
    }
    
    # Header styles
    if "columns" in table_component:
        for column in table_component["columns"]:
            column["header_style"] = TABLE_STYLES["header"]
    
    # Row styles
    table_component["row_style"] = TABLE_STYLES["row"]
    table_component["row_hover_style"] = TABLE_STYLES["row"]["hover"]
    table_component["row_selected_style"] = TABLE_STYLES["row_selected"]
    
    return table_component

def apply_dashboard_styles(dashboard_component: Dict[str, Any]) -> Dict[str, Any]:
    """Apply consistent dashboard styling"""
    dashboard_component["style"] = {
        "background": COLORS["light"],
        "padding": "16px",
        "border_radius": "8px",
        "box_shadow": "0 2px 8px rgba(0,0,0,0.1)"
    }
    
    return dashboard_component

# CSS-like styling utilities
def create_css_styles() -> str:
    """Generate CSS styles for the Qanat UI"""
    return f"""
/* Qanat UI Styles */
.qanat-dashboard {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background: {COLORS['light']};
    padding: 16px;
    border-radius: 8px;
}}

.qanat-table {{
    width: 100%;
    border-collapse: collapse;
    background: {COLORS['white']};
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}

.qanat-table th {{
    background: {COLORS['light']};
    color: {COLORS['dark']};
    font-weight: 600;
    padding: 12px;
    text-align: left;
    border-bottom: 2px solid {COLORS['gray']};
}}

.qanat-table td {{
    padding: 12px;
    border-bottom: 1px solid {COLORS['light']};
}}

.qanat-table tr:hover {{
    background: {COLORS['light']};
}}

.qanat-badge {{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}}

.qanat-badge-success {{
    background: {COLORS['success_bg']};
    color: {COLORS['success_text']};
    border: 1px solid {COLORS['success']};
}}

.qanat-badge-warning {{
    background: {COLORS['warning_bg']};
    color: {COLORS['warning_text']};
    border: 1px solid {COLORS['warning']};
}}

.qanat-badge-error {{
    background: {COLORS['error_bg']};
    color: {COLORS['error_text']};
    border: 1px solid {COLORS['error']};
}}

.qanat-button {{
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.2s ease;
}}

.qanat-button-primary {{
    background: {COLORS['primary']};
    color: {COLORS['white']};
}}

.qanat-button-primary:hover {{
    background: #0056b3;
}}

.qanat-button-secondary {{
    background: {COLORS['secondary']};
    color: {COLORS['white']};
}}

.qanat-button-success {{
    background: {COLORS['success']};
    color: {COLORS['white']};
}}

.qanat-button-warning {{
    background: {COLORS['warning']};
    color: {COLORS['dark']};
}}

.qanat-loading {{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.qanat-spinner {{
    width: 24px;
    height: 24px;
    border: 3px solid {COLORS['light']};
    border-top: 3px solid {COLORS['primary']};
    border-radius: 50%;
    animation: qanat-spin 1s linear infinite;
}}

@keyframes qanat-spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

.qanat-notification {{
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}

.qanat-notification-success {{
    background: {COLORS['success_bg']};
    color: {COLORS['success_text']};
    border: 1px solid {COLORS['success']};
}}

.qanat-notification-warning {{
    background: {COLORS['warning_bg']};
    color: {COLORS['warning_text']};
    border: 1px solid {COLORS['warning']};
}}

.qanat-notification-error {{
    background: {COLORS['error_bg']};
    color: {COLORS['error_text']};
    border: 1px solid {COLORS['error']};
}}

.qanat-notification-info {{
    background: {COLORS['info_bg']};
    color: {COLORS['info_text']};
    border: 1px solid {COLORS['info']};
}}
"""

# Export styling functions
__all__ = [
    "COLORS",
    "get_status_badge_style", 
    "get_button_style",
    "create_styled_badge",
    "create_styled_button", 
    "create_loading_overlay",
    "create_notification",
    "apply_table_styles",
    "apply_dashboard_styles",
    "create_css_styles"
]
