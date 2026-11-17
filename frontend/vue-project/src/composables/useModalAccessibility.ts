import { ref, watch, nextTick, type Ref } from 'vue';

export interface UseModalAccessibilityOptions {
  isOpen: Ref<boolean>;
  modalRef: Ref<HTMLElement | null>;
  onClose: () => void;
  initialFocusRef?: Ref<HTMLElement | null>;
}

export function useModalAccessibility({
  isOpen,
  modalRef,
  onClose,
  initialFocusRef,
}: UseModalAccessibilityOptions) {
  const triggerElement = ref<HTMLElement | null>(null);

  function getFocusableElements(container: HTMLElement): HTMLElement[] {
    const selector =
      'button:not(:disabled), [href], input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])';
    return Array.from(container.querySelectorAll<HTMLElement>(selector)).filter(
      (el) => el.offsetParent !== null && !el.hasAttribute('disabled')
    );
  }

  function handleKeydown(e: KeyboardEvent) {
    if (!isOpen.value || !modalRef.value) return;

    if (e.key === 'Escape') {
      e.preventDefault();
      e.stopPropagation();
      onClose();
      return;
    }

    if (e.key === 'Tab') {
      const focusables = getFocusableElements(modalRef.value);
      if (focusables.length === 0) {
        e.preventDefault();
        return;
      }

      const first = focusables[0]!;
      const last = focusables[focusables.length - 1]!;

      if (e.shiftKey) {
        if (document.activeElement === first || !modalRef.value.contains(document.activeElement)) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (document.activeElement === last || !modalRef.value.contains(document.activeElement)) {
          e.preventDefault();
          first.focus();
        }
      }
    }
  }

  function lockBodyScroll() {
    const scrollBarWidth = window.innerWidth - document.documentElement.clientWidth;
    if (scrollBarWidth > 0) {
      document.body.style.paddingRight = `${scrollBarWidth}px`;
    }
    document.body.style.overflow = 'hidden';
  }

  function unlockBodyScroll() {
    document.body.style.paddingRight = '';
    document.body.style.overflow = '';
  }

  watch(
    () => isOpen.value,
    async (open) => {
      if (open) {
        // Save current active element to restore focus later
        if (document.activeElement instanceof HTMLElement) {
          triggerElement.value = document.activeElement;
        }

        lockBodyScroll();
        window.addEventListener('keydown', handleKeydown);

        await nextTick();

        // Focus initial element or first focusable
        if (initialFocusRef?.value) {
          initialFocusRef.value.focus();
        } else if (modalRef.value) {
          const focusables = getFocusableElements(modalRef.value);
          if (focusables.length > 0) {
            focusables[0]?.focus();
          } else {
            modalRef.value.focus();
          }
        }
      } else {
        unlockBodyScroll();
        window.removeEventListener('keydown', handleKeydown);

        // Restore focus to trigger
        await nextTick();
        if (triggerElement.value && document.body.contains(triggerElement.value)) {
          triggerElement.value.focus();
        }
        triggerElement.value = null;
      }
    }
  );

  return {
    triggerElement,
  };
}
