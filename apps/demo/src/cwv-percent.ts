import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';

/**
 * @slot - This element has a slot
 */
@customElement('cwv-percent')
export class CWVPercent extends LitElement {
  @property() value: number = 0;

  static styles = css`
    :host {
      --_cwv-percent-good: var(--cwv-percent-bg-good, #c9fbeb);
      --_cwv-percent-ni: var(--cwv-percent-bg-ni, #fff5c2);
      --_cwv-percent-poor: var(--cwv-percent-bg-poor, #fde0db);
      display: block;
    }

    .bar {
      display: block;
      padding-left: 0.25rem;
      background: none;
    }
  `;

  protected updated(changed: any): void {
    if (changed.has('value') && !!this.value) {
      const cleanValue = Math.min(this.value, 100);

      // Set the linear gradient as the background
      const style = this.calculateBarGraph(cleanValue);
      if (style) {
        this.style.setProperty('background', style);
      }
    }
  }

  calculateBarGraph(value: number): string | undefined {
    if (value <= 0) {
      return;
    }

    let color:
      | 'var(--_cwv-percent-poor)'
      | 'var(--_cwv-percent-ni)'
      | 'var(--_cwv-percent-good)' = 'var(--_cwv-percent-poor)';

    if (value >= 75) {
      color = 'var(--_cwv-percent-good)';
    } else if (value >= 66.67) {
      color = 'var(--_cwv-percent-ni)';
    }

    return `linear-gradient(90deg, ${color} 0%, ${color} ${value}%, transparent ${value}%)`;
  }

  render() {
    return html`
      <span class="bar">
        <slot></slot>
      </span>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'cwv-percent': CWVPercent;
  }
}
