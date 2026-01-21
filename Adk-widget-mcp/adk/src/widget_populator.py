"""
Widget Populator for ADK
Populates widget schemas with actual data based on context
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List
import copy


class WidgetPopulator:
    """Populates widget schemas with real data"""
    
    TIMEZONES = [
        {"label": "Eastern Time (ET)", "value": "ET", "offset": "-05:00"},
        {"label": "Central Time (CT)", "value": "CT", "offset": "-06:00"},
        {"label": "Mountain Time (MT)", "value": "MT", "offset": "-07:00"},
        {"label": "Pacific Time (PT)", "value": "PT", "offset": "-08:00"},
    ]
    
    def populate_schedule_meeting_widget(self, schema: dict, context: dict) -> dict:
        """Populate schedule meeting widget with dates and times"""
        widget = copy.deepcopy(schema)
        
        # Set timezone
        tz_value = context.get("timezone", "Eastern Time (ET)")
        tz_abbr = context.get("timezone_abbr", "ET")
        widget["properties"]["timezone"]["value"] = tz_value
        
        # Populate dates
        dates = self._get_next_dates(5)
        widget["properties"]["date_selector"]["options"] = [
            {
                "label": date["day"],
                "sublabel": date["date_str"],
                "value": date["value"],
                "selected": date["value"] == context.get("selected_date_value")
            }
            for date in dates
        ]
        
        # Populate time slots
        times = self._get_time_slots(tz_abbr)
        widget["properties"]["time_slots"]["options"] = [
            {
                "label": time["label"],
                "value": time["value"],
                "selected": time["value"] == context.get("selected_time_value")
            }
            for time in times
        ]
        
        # Enable schedule button if both date and time selected
        has_selections = (
            context.get("selected_date_value") and 
            context.get("selected_time_value")
        )
        widget["properties"]["actions"]["buttons"][0]["enabled"] = has_selections
        
        return widget
    
    def populate_timezone_selector_widget(self, schema: dict, context: dict) -> dict:
        """Populate timezone selector with available timezones"""
        widget = copy.deepcopy(schema)
        
        current_tz_abbr = context.get("timezone_abbr", "ET")
        
        widget["properties"]["timezone_list"]["options"] = [
            {
                "label": tz["label"],
                "value": tz["value"],
                "selected": tz["value"] == current_tz_abbr
            }
            for tz in self.TIMEZONES
        ]
        
        return widget
    
    def _get_next_dates(self, count: int) -> List[Dict[str, str]]:
        """Get next N business days"""
        dates = []
        current = datetime.now()
        
        while len(dates) < count:
            # Skip weekends
            if current.weekday() < 5:  # Monday = 0, Friday = 4
                dates.append({
                    "day": current.strftime("%a").upper(),
                    "date_str": current.strftime("%b %d"),
                    "value": current.strftime("%Y-%m-%d")
                })
            current += timedelta(days=1)
        
        return dates
    
    def _get_time_slots(self, timezone_abbr: str) -> List[Dict[str, str]]:
        """Get available time slots"""
        return [
            {"label": f"11:30 AM {timezone_abbr}", "value": "11:30"},
            {"label": f"1:45 PM {timezone_abbr}", "value": "13:45"},
            {"label": f"3:00 PM {timezone_abbr}", "value": "15:00"}
        ]
    
    def get_timezone_by_abbr(self, abbr: str) -> Dict[str, str]:
        """Get timezone details by abbreviation"""
        for tz in self.TIMEZONES:
            if tz["value"] == abbr:
                return tz
        return self.TIMEZONES[0]  # Default to ET


def get_widget_populator() -> WidgetPopulator:
    """Get widget populator instance"""
    return WidgetPopulator()
