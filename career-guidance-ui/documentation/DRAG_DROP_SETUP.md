# Drag-and-Drop Section Reordering Setup Guide

## Status: Architecture Prepared, Installation Required

The drag-and-drop functionality is architecturally prepared but requires package installation to complete.

---

## Step 1: Install Required Packages

Run this command in the `career-guidance-ui` directory:

```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

Or with yarn:

```bash
yarn add @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

---

## Step 2: Create SectionReorderList Component

Create `career-guidance-ui/src/components/resume/SectionReorderList.jsx`:

```jsx
import { DndContext, closestCenter, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical } from 'lucide-react';

const SortableSection = ({ id, children }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div ref={setNodeRef} style={style} className="flex items-center space-x-2 mb-2">
      <button
        {...attributes}
        {...listeners}
        className="p-2 glass rounded-lg hover:glow-cyan transition-all duration-300 cursor-grab active:cursor-grabbing"
      >
        <GripVertical size={18} className="text-gray-400" />
      </button>
      <div className="flex-1">{children}</div>
    </div>
  );
};

const SectionReorderList = ({ sections, onReorder }) => {
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  const handleDragEnd = (event) => {
    const { active, over } = event;

    if (active.id !== over.id) {
      const oldIndex = sections.findIndex((s) => s.id === active.id);
      const newIndex = sections.findIndex((s) => s.id === over.id);

      const newSections = [...sections];
      const [removed] = newSections.splice(oldIndex, 1);
      newSections.splice(newIndex, 0, removed);

      onReorder(newSections);
    }
  };

  return (
    <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
      <SortableContext items={sections.map((s) => s.id)} strategy={verticalListSortingStrategy}>
        <div className="glass rounded-lg p-4 mb-4">
          <h3 className="text-lg font-semibold text-white mb-3">Reorder Sections</h3>
          {sections.map((section) => (
            <SortableSection key={section.id} id={section.id}>
              <span className="text-white">{section.label}</span>
            </SortableSection>
          ))}
        </div>
      </SortableContext>
    </DndContext>
  );
};

export default SectionReorderList;
```

---

## Step 3: Update BuildResume.jsx

Add section order state and integrate the component:

```jsx
import SectionReorderList from '../components/resume/SectionReorderList';

// Inside BuildResume component, add state:
const [sectionOrder, setSectionOrder] = useState([
  { id: 'summary', label: 'Professional Summary' },
  { id: 'skills', label: 'Skills' },
  { id: 'experience', label: 'Experience' },
  { id: 'education', label: 'Education' },
  { id: 'projects', label: 'Projects' },
  { id: 'certifications', label: 'Certifications' },
  { id: 'achievements', label: 'Achievements' },
]);

// Add handler:
const handleSectionReorder = (newOrder) => {
  setSectionOrder(newOrder);
};

// Add component in the form section (before ResumeForm):
<SectionReorderList sections={sectionOrder} onReorder={handleSectionReorder} />
```

---

## Step 4: Update ResumePreview.jsx

Modify templates to respect section order:

```jsx
const ResumePreview = ({ resumeData, template, previewMode = false, previewTheme = 'light', sectionOrder }) => {
  // Pass sectionOrder to templates
  return (
    // ... existing code
    <ModernTemplate data={resumeData} theme={previewTheme} sectionOrder={sectionOrder} />
  );
};

// In ModernTemplate:
const ModernTemplate = ({ data, theme = 'light', sectionOrder = [] }) => {
  const renderSection = (sectionId) => {
    switch (sectionId) {
      case 'summary':
        return data.summary && (
          <div key="summary">
            <h2>PROFESSIONAL SUMMARY</h2>
            <p>{data.summary}</p>
          </div>
        );
      case 'skills':
        return data.skills.length > 0 && (
          <div key="skills">
            <h2>SKILLS</h2>
            {/* skills content */}
          </div>
        );
      // ... other sections
      default:
        return null;
    }
  };

  return (
    <div className="space-y-4">
      {/* Header (always first) */}
      <div>...</div>
      
      {/* Ordered sections */}
      {sectionOrder.map((section) => renderSection(section.id))}
    </div>
  );
};
```

---

## Step 5: Update BuildResume.jsx Preview Section

Pass sectionOrder to ResumePreview:

```jsx
<ResumePreview 
  resumeData={resumeData} 
  template={selectedTemplate}
  previewMode={true}
  previewTheme={previewTheme}
  sectionOrder={sectionOrder}
/>
```

---

## Features After Implementation

1. ✅ Drag handle icon on each section
2. ✅ Smooth drag animation
3. ✅ Visual feedback during drag
4. ✅ Instant preview update
5. ✅ Maintains ATS-friendly structure
6. ✅ Works with all templates
7. ✅ Persists during theme changes

---

## Testing

After implementation, test:
1. Drag sections up and down
2. Verify preview updates immediately
3. Check all templates respect new order
4. Ensure exports maintain the order
5. Test with empty sections
6. Verify mobile responsiveness

---

## Notes

- The drag activation requires 8px movement to prevent accidental drags
- Cursor changes to "grab" on hover, "grabbing" when dragging
- Sections with no content are still reorderable
- Header (personal info) always stays at the top
- Export maintains the custom order

---

## Alternative: Manual Implementation

If you prefer not to use @dnd-kit, you can implement basic reordering with:
1. Up/Down arrow buttons
2. Simple array manipulation
3. No drag-and-drop library required

Example:
```jsx
const moveSection = (index, direction) => {
  const newOrder = [...sectionOrder];
  const newIndex = direction === 'up' ? index - 1 : index + 1;
  
  if (newIndex >= 0 && newIndex < newOrder.length) {
    [newOrder[index], newOrder[newIndex]] = [newOrder[newIndex], newOrder[index]];
    setSectionOrder(newOrder);
  }
};
```

---

## Estimated Time

- Package installation: 1 minute
- Component creation: 15 minutes
- Integration: 10 minutes
- Testing: 10 minutes
- Total: ~35 minutes

---

## Support

If you encounter issues:
1. Check @dnd-kit documentation: https://docs.dndkit.com/
2. Verify package versions are compatible
3. Check browser console for errors
4. Ensure React version is compatible (19.2.4 ✅)
