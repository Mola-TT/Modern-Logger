from PySide6.QtWidgets import QTextEdit, QLabel, QApplication
from PySide6.QtCore import Qt, Signal, Slot, QTimer
from PySide6.QtGui import QTextCursor
from datetime import datetime
import queue
import re
import traceback
import sys

class ModernLogger(QTextEdit):
    """
    A QTextEdit-based modern logger that displays timestamped messages
    and supports a non-blocking loading indicator.
    """
    
    scroll_state_changed = Signal(bool)  # True when at bottom, False when scrolled up

    def __init__(self, parent=None, queue_messages=True):
        super().__init__(parent)
        self.setReadOnly(True)
        
        # Document configuration
        doc = self.document()
        doc.setDocumentMargin(8)
        doc.setUndoRedoEnabled(False)
        doc.setMaximumBlockCount(5000)
        
        # Loading indicator settings
        self._loading = False
        self._loading_timer = QTimer(self)
        self._loading_timer.timeout.connect(self._update_loading)
        self._loading_dots = 0
        self._loading_line_index = -1  # Track loading indicator line index
        
        # Message queue settings
        self._queue_messages = queue_messages
        self._passthrough_messages = False
        self._message_queue = queue.Queue()
        
        # Timestamp format
        self._timestamp_format = "[%Y-%m-%d %H:%M:%S]"
        
        # Batch processing
        self._batch_timer = QTimer(self)
        self._batch_timer.setSingleShot(True)
        self._batch_timer.timeout.connect(self._process_batch)
        self._pending_batch = []
        
        # Scroll management
        self._auto_scroll_enabled = True
        self._user_has_scrolled = False
        self._last_known_position = 0
        self._was_at_bottom = True  # Start assuming at bottom
        
        # Connect scroll signals
        scrollbar = self.verticalScrollBar()
        scrollbar.valueChanged.connect(self._on_scroll)
        scrollbar.sliderPressed.connect(self._on_user_scroll_start)
        scrollbar.sliderReleased.connect(self._on_user_scroll_end)
        
        # Visual indicator for auto-scroll state
        self._add_scroll_indicator()
        
        # First-run flag
        self._first_content = True
    
    def _add_scroll_indicator(self):
        """Add indicator showing auto-scroll state"""
        self._scroll_indicator = QLabel(self)
        self._scroll_indicator.setStyleSheet(
            "background-color: rgba(0, 0, 0, 100); "
            "color: white; padding: 2px; border-radius: 2px;"
        )
        self._scroll_indicator.setText("Auto-scroll: On")
        self._scroll_indicator.adjustSize()
        self._scroll_indicator.hide()
        self.scroll_state_changed.connect(self._update_indicator)
    
    def _update_indicator(self, auto_scroll_on):
        """Update the scroll indicator appearance"""
        if auto_scroll_on:
            self._scroll_indicator.hide()
        else:
            self._scroll_indicator.setText("Auto-scroll: Paused")
            self._scroll_indicator.adjustSize()
            margin = 10
            self._scroll_indicator.move(
                self.width() - self._scroll_indicator.width() - margin,
                self.height() - self._scroll_indicator.height() - margin
            )
            self._scroll_indicator.show()
    
    def resizeEvent(self, event):
        """Handle resize to update indicator position"""
        super().resizeEvent(event)
        if hasattr(self, '_scroll_indicator'):
            margin = 10
            self._scroll_indicator.move(
                self.width() - self._scroll_indicator.width() - margin,
                self.height() - self._scroll_indicator.height() - margin
            )
    
    def _is_at_bottom(self):
        """Check if view is scrolled to bottom"""
        scrollbar = self.verticalScrollBar()
        return scrollbar.value() >= scrollbar.maximum() - 5
    
    def _on_user_scroll_start(self):
        """Handle when user begins manual scrolling"""
        self._user_has_scrolled = True
        self._last_known_position = self.verticalScrollBar().value()
    
    def _on_user_scroll_end(self):
        """Handle when user finishes manual scrolling"""
        # Check if we're at bottom after user scrolling
        at_bottom = self._is_at_bottom()
        
        # Enable auto-scroll if user scrolled to bottom
        if at_bottom and not self._auto_scroll_enabled:
            self._auto_scroll_enabled = True
            self.scroll_state_changed.emit(True)
        
        self._user_has_scrolled = False
        self._was_at_bottom = at_bottom
    
    def _on_scroll(self, value):
        """Track scroll position changes"""
        # Only detect user scrolling away from bottom
        if self._user_has_scrolled:
            was_at_bottom = self._was_at_bottom
            now_at_bottom = self._is_at_bottom()
            
            # If user scrolled away from bottom
            if was_at_bottom and not now_at_bottom:
                self._auto_scroll_enabled = False
                self.scroll_state_changed.emit(False)
            
            # If user scrolled back to bottom
            elif not was_at_bottom and now_at_bottom:
                self._auto_scroll_enabled = True
                self.scroll_state_changed.emit(True)
            
            # Update state
            self._was_at_bottom = now_at_bottom
    
    def _do_auto_scroll(self):
        """Perform auto-scrolling if enabled"""
        if not self._auto_scroll_enabled:
            return False
        
        # Reset text cursor to end
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        
        # Set scrollbar to maximum
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # Force immediate update
        self.repaint()
        QApplication.processEvents()
        
        return True
    
    def append_message(self, text):
        """Add a timestamped message"""
        try:
            # Create timestamp
            timestamp = datetime.now().strftime(self._timestamp_format + " ")
            full_message = f"{timestamp}{text}"
            
            # Queue or batch based on mode
            if self._loading and self._queue_messages and not self._passthrough_messages:
                self._message_queue.put(full_message)
            else:
                self._pending_batch.append(full_message)
                
                # Process immediately or schedule
                if len(self._pending_batch) == 1:
                    self._batch_timer.start(0)
                elif len(self._pending_batch) >= 10:
                    self._batch_timer.stop()
                    self._process_batch()
        except Exception as e:
            print(f"Error in append_message: {traceback.format_exc()}", file=sys.stderr)
    
    def append(self, text):
        """Overridden append method"""
        # Use built-in append
        super().append(text)
        
        # Auto-scroll as needed
        if self._auto_scroll_enabled:
            self._do_auto_scroll()
    
    def _force_append_at_end(self, text):
        """Append text ensuring it's at the end, even with loading indicator"""
        current_text = self.toPlainText()
        lines = current_text.strip().split('\n')
        
        # Check if the last line is a loading indicator
        loading_line_index = -1
        for i in range(len(lines)-1, -1, -1):
            if "Loading" in lines[i] and not any(x in lines[i] for x in ["completed", "stopped"]):
                loading_line_index = i
                break
        
        if loading_line_index >= 0:
            # Remove loading line
            loading_line = lines.pop(loading_line_index)
            
            # Add new line + loading line
            lines.append(text)
            lines.append(loading_line)
            
            # Update text
            self.setPlainText('\n'.join(lines))
        else:
            # Normal append
            super().append(text)
        
        # Auto-scroll as needed
        if self._auto_scroll_enabled:
            self._do_auto_scroll()
    
    def _process_batch(self):
        """Process pending message batch"""
        try:
            if not self._pending_batch:
                return
            
            # Save scroll info
            was_scrollbar_at_bottom = self._is_at_bottom()
            
            if self._loading and self._passthrough_messages:
                # Handle loading indicator specially for passthrough mode
                
                # 1. Get current content without loading indicator
                content = self.toPlainText()
                lines = content.split('\n')
                
                # 2. Find and remove loading indicator
                loading_indices = []
                for i, line in enumerate(lines):
                    if "Loading" in line and not any(x in line for x in ["completed", "stopped"]):
                        loading_indices.append(i)
                
                # 3. Remove loading indicators
                if loading_indices:
                    # Filter out loading lines
                    filtered_lines = [line for i, line in enumerate(lines) if i not in loading_indices]
                    
                    # Add batch messages
                    for message in self._pending_batch:
                        filtered_lines.append(message)
                    
                    # Add new loading indicator at the end
                    timestamp = datetime.now().strftime(self._timestamp_format + " ")
                    dots = '.' * self._loading_dots
                    filtered_lines.append(f"{timestamp}Loading{dots}")
                    
                    # Update text
                    self.setPlainText('\n'.join(filtered_lines))
                else:
                    # No loading indicator found (shouldn't happen, but handle it)
                    for message in self._pending_batch:
                        super().append(message)
                    
                    # Add loading indicator at end
                    timestamp = datetime.now().strftime(self._timestamp_format + " ")
                    dots = '.' * self._loading_dots
                    super().append(f"{timestamp}Loading{dots}")
            else:
                # Normal mode - just append messages
                for message in self._pending_batch:
                    super().append(message)
            
            # Clear batch
            self._pending_batch.clear()
            
            # Auto-scroll if needed
            if self._auto_scroll_enabled and (was_scrollbar_at_bottom or self._first_content):
                self._do_auto_scroll()
                self._first_content = False
                
        except Exception as e:
            print(f"Error in _process_batch: {traceback.format_exc()}", file=sys.stderr)
            self._pending_batch.clear()
    
    def set_loading_on(self, queue_messages=None, passthrough_messages=False):
        """Activate the loading indicator"""
        try:
            # Stop existing loading
            if self._loading:
                self._loading = False
                self._loading_timer.stop()
            
            # Update settings
            if queue_messages is not None:
                self._queue_messages = queue_messages
            self._passthrough_messages = passthrough_messages
            
            # Process pending messages
            self._process_batch()
            
            # Set loading state
            self._loading = True
            self._loading_dots = 0
            
            # Add initial loading indicator
            timestamp = datetime.now().strftime(self._timestamp_format + " ")
            super().append(f"{timestamp}Loading")
            
            # Start animation
            self._loading_timer.start(500)
            
            # Force scroll to end
            self._do_auto_scroll()
            
            # Schedule additional scroll after layout completes
            QTimer.singleShot(100, self._do_auto_scroll)
            
        except Exception as e:
            print(f"Error in set_loading_on: {traceback.format_exc()}", file=sys.stderr)
    
    def set_loading_off(self, completion_message=None):
        """Deactivate the loading indicator"""
        try:
            if not self._loading:
                return
            
            # Update state
            self._loading = False
            self._loading_timer.stop()
            self._loading_line_index = -1
            
            # Remove loading indicators
            self._remove_loading_indicators()
            
            # Process queued messages
            if not self._message_queue.empty():
                messages = []
                while not self._message_queue.empty():
                    try:
                        messages.append(self._message_queue.get(block=False))
                    except queue.Empty:
                        break
                
                for message in messages:
                    super().append(message)
                    
                # Process events periodically
                QApplication.processEvents()
            
            # Add completion message
            if completion_message is not None:
                timestamp = datetime.now().strftime(self._timestamp_format + " ")
                super().append(f"{timestamp}{completion_message}")
            elif completion_message is None:  # Only if None (not empty string)
                timestamp = datetime.now().strftime(self._timestamp_format + " ")
                super().append(f"{timestamp}Loading operation completed")
            
            # Auto-scroll as needed
            if self._auto_scroll_enabled:
                self._do_auto_scroll()
                
        except Exception as e:
            print(f"Error in set_loading_off: {traceback.format_exc()}", file=sys.stderr)
    
    def _remove_loading_indicators(self):
        """Remove all loading indicator lines"""
        try:
            # Get current content
            content = self.toPlainText()
            lines = content.split('\n')
            
            # Filter out loading indicators
            filtered_lines = []
            found_indicator = False
            
            for line in lines:
                if "Loading" in line and not any(x in line for x in ["completed", "stopped"]):
                    found_indicator = True
                    continue
                if line.strip():  # Keep non-empty lines
                    filtered_lines.append(line)
            
            # Update content if indicators were found
            if found_indicator:
                self.setPlainText('\n'.join(filtered_lines))
                
            return found_indicator
            
        except Exception as e:
            print(f"Error removing loading indicators: {traceback.format_exc()}", file=sys.stderr)
            return False
    
    @Slot()
    def _update_loading(self):
        """Update the loading indicator animation"""
        if not self._loading:
            return
            
        try:
            # Update animation dots
            self._loading_dots = (self._loading_dots + 1) % 4
            dots = '.' * self._loading_dots
            
            # For passthrough mode, let batch processor handle it
            if self._passthrough_messages and self._pending_batch:
                self._process_batch()
                return
            
            # Block signals during update
            scrollbar = self.verticalScrollBar()
            was_at_bottom = self._is_at_bottom()
            scrollbar.blockSignals(True)
            
            try:
                # Get current content
                content = self.toPlainText()
                lines = content.split('\n')
                found_loading = False
                
                # Find and update the last loading indicator
                for i in range(len(lines)-1, -1, -1):
                    if "Loading" in lines[i] and not any(x in lines[i] for x in ["completed", "stopped"]):
                        # Extract timestamp
                        timestamp_end = lines[i].find("]") + 2 if "]" in lines[i] else 0
                        timestamp = lines[i][:timestamp_end] if timestamp_end > 0 else ""
                        
                        # Replace with updated dots
                        lines[i] = f"{timestamp}Loading{dots}"
                        found_loading = True
                        break
                
                # If no loading line found, add one
                if not found_loading:
                    timestamp = datetime.now().strftime(self._timestamp_format + " ")
                    lines.append(f"{timestamp}Loading{dots}")
                
                # Update text
                self.setPlainText('\n'.join(lines))
                
                # Auto-scroll if needed
                if self._auto_scroll_enabled and was_at_bottom:
                    cursor = self.textCursor()
                    cursor.movePosition(QTextCursor.End)
                    self.setTextCursor(cursor)
                    scrollbar.setValue(scrollbar.maximum())
                
            finally:
                # Restore signals
                scrollbar.blockSignals(False)
                
        except Exception as e:
            print(f"Error updating loading indicator: {traceback.format_exc()}", file=sys.stderr)
    
    def simulate_work_mode(self, enable):
        """
        Compatibility method for existing code that uses this method.
        No special handling needed in the new implementation.
        """
        # No special handling needed in the new implementation
        # This method is kept for backwards compatibility
        pass
