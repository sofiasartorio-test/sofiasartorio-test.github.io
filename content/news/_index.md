---
title: 'Talks & Events'
type: landing

sections:
  - block: collection
    content:
      title: Upcoming Events
      filters:
        folders:
          - event
        future: true
      sort_by: date
      sort_ascending: true
      count: 5
    design:
      view: card

  - block: collection
    content:
      title: Past Events
      filters:
        folders:
          - event
        past: true
      sort_by: date
      sort_ascending: false
      count: 5
    design:
      view: card
---
